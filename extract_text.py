"""Parse EUR-Lex HTML (GDPR, AI Act) into structured units: recitals and articles.

Output is JSONL, one unit per line, in document order:
  {"doc": "gdpr", "kind": "recital", "number": "26", "title": "", "text": "..."}
  {"doc": "gdpr", "kind": "article", "article": "33", "title": "Notification of ...", "text": "..."}

Run from the repo root:   python extract_text.py
"""

import json
import re
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

# Sanity-check targets. If one fails, first compare with the official text before changing the code.
EXPECTED = {
    "gdpr": {"recital": 173, "article": 99},
    "ai_act": {"recital": 180, "article": 113},
}

# An article's content stops when a sibling element with one of these classes starts.
STOP_CLASSES = {"oj-ti-art", "oj-ti-section-1", "oj-ti-section-2", "oj-doc-end", "oj-signatory"}


def clean(text: str) -> str:
    """Normalise whitespace left over from HTML (nbsp, line breaks, spaces before punctuation)."""
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:)])", r"\1", text)  # "word ," -> "word,"
    text = re.sub(r"\(\s+", "(", text)  # "( a" -> "(a"
    return text


def extract_recitals(soup: BeautifulSoup, doc_name: str) -> list[dict]:
    """Return recitals as {number: text}, without duplicates.

    Why this is more careful than a plain "match text starting with (1)":
    in EUR-Lex HTML the number "(1)" and the recital text sit in different table cells, inside one
    wrapper <div>. A scan over every <div> and <p> then finds each recital twice: once as the
    wrapper (full text) and once as the number-only <p> (empty text). We avoid that by keying on the
    recital number and keeping one entry per number.
    """
    found: dict[int, str] = {}

    # Preferred route: EUR-Lex marks each recital wrapper with id="rct_<n>".
    wrappers = soup.find_all(id=re.compile(r"^rct_\d+$"))
    if wrappers:
        for w in wrappers:
            num = int(w["id"].split("_")[1])
            text = clean(w.get_text(" ", strip=True))
            text = re.sub(r"^\(\s*\d+\s*\)\s*", "", text)  # drop the leading "(n)"
            found[num] = text
    else:
        # Fallback when the ids are absent: scan the preamble, keep the SHORTEST non-empty body
        # per number (a wrapper around many recitals would be longer, an empty <p> is skipped).
        first_article = soup.find(class_="oj-ti-art")
        whereas = soup.find(string=re.compile(r"Whereas"))
        elements = whereas.find_parent().find_all_next(["div", "p"]) if whereas else soup.find_all(["div", "p"])
        for el in elements:
            if el is first_article:
                break
            m = re.match(r"^\((\d+)\)\s*(.*)", clean(el.get_text(" ", strip=True)))
            if not m or not m.group(2):
                continue
            num, body = int(m.group(1)), m.group(2)
            if num not in found or len(body) < len(found[num]):
                found[num] = body

    return [
        {"doc": doc_name, "kind": "recital", "number": str(n), "title": "", "text": found[n]}
        for n in sorted(found)
    ]


def extract_articles(soup: BeautifulSoup, doc_name: str) -> list[dict]:
    units = []
    for art_tag in soup.find_all(class_="oj-ti-art"):
        art_num = re.sub(r"^Article\s+", "", clean(art_tag.get_text(strip=True)))

        # The element right after "Article N" is the title, if it carries a title class.
        title = ""
        next_el = art_tag.find_next_sibling()
        is_title = False
        if next_el is not None:
            classes = " ".join(next_el.get("class") or [])
            if "eli-title" in classes or "oj-sti-art" in classes:
                title = clean(next_el.get_text(" ", strip=True))
                is_title = True

        # Collect paragraphs until the next article / chapter / section / signature block.
        cursor = next_el.find_next_sibling() if is_title else next_el
        paragraphs = []
        while cursor is not None:
            if set(cursor.get("class") or []) & STOP_CLASSES:
                break
            text = clean(cursor.get_text(" ", strip=True))
            if text:
                paragraphs.append(text)
            cursor = cursor.find_next_sibling()

        units.append(
            {"doc": doc_name, "kind": "article", "article": art_num, "title": title, "text": "\n".join(paragraphs)}
        )
    return units


def extract_units(html_path: str, doc_name: str) -> list[dict]:
    """Parse one EUR-Lex HTML file into recital units followed by article units."""
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for note in soup.find_all(class_="oj-note"):  # footnote bodies
        note.decompose()

    return extract_recitals(soup, doc_name) + extract_articles(soup, doc_name)


def validate(units: list[dict], doc_name: str) -> None:
    """Fail loudly on anything suspicious instead of passing silently."""
    counts = Counter(u["kind"] for u in units)
    for kind, expected in EXPECTED[doc_name].items():
        assert counts[kind] == expected, (
            f"{doc_name}: expected {expected} {kind}s, got {counts[kind]} (compare with the official text)"
        )

    empty = [u.get("number") or u.get("article") for u in units if not u["text"].strip()]
    assert not empty, f"{doc_name}: empty units: {empty[:10]}"

    rec = [int(u["number"]) for u in units if u["kind"] == "recital"]
    assert rec == list(range(1, len(rec) + 1)), f"{doc_name}: recital numbers are not 1..N"
    art = [int(u["article"]) for u in units if u["kind"] == "article"]
    assert art == list(range(1, len(art) + 1)), f"{doc_name}: article numbers are not 1..N"

    # Soft check (warning only): leftover footnote markers look like "Directive(1)".
    marker = re.compile(r"[A-Za-z]\(\d+\)")
    hits = [(u.get("number") or u.get("article"), m.group()) for u in units for m in marker.finditer(u["text"])]
    if hits:
        print(f"  warning: {len(hits)} possible footnote markers, e.g. {hits[:5]}")


def main():
    raw_dir = Path("data/raw")
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    for doc_name in ("gdpr", "ai_act"):
        html_path = raw_dir / f"{doc_name}.html"
        out_path = out_dir / f"{doc_name}.jsonl"
        if not html_path.exists():
            print(f"file does not exist: {html_path}")
            continue

        units = extract_units(str(html_path), doc_name)
        with open(out_path, "w", encoding="utf-8") as f:  # write first, so you can inspect even if validation fails
            for u in units:
                f.write(json.dumps(u, ensure_ascii=False) + "\n")

        counts = Counter(u["kind"] for u in units)
        print(f"{doc_name}: {counts['article']} articles, {counts['recital']} recitals -> {out_path}")

        validate(units, doc_name)

        # Eyeball samples: compare these with the official website.
        first_rec = next(u for u in units if u["kind"] == "recital")
        art33 = next((u for u in units if u["kind"] == "article" and u["article"] == "5"), None)
        print("  recital 1 :", first_rec["text"][:150])
        if art33:
            print("  article 5 :", art33["title"], "|", art33["text"][:150].replace("\n", " / "))


if __name__ == "__main__":
    main()
