import json
import os
import re 
from bs4 import BeautifulSoup
from pathlib import Path

# def extract_text(html_path, text_path):
#     with open(html_path, 'r', encoding = 'utf-8') as f:
#         soup = BeautifulSoup(f.read(), 'html.parser')

#     for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
#         tag.decompose()

#     text = soup.get_text(separator = '\n', strip = True)
#     lines = [line.strip() for line in text.splitlines() if line.strip()]

#     start_idx = 0
#     for i, line in enumerate(lines):
#         if line.startswith("REGULATION (EU)") or line.startswith("REGULATION (EU) 2016/679") or "Artificial Intelligence Act" in line:
#             start_idx = i
#             break

#     lines = lines[start_idx:]

#     cleaned = []
#     buffer = ''
    
#     for line in lines:
#         if "Official Journal of the European Union" in line:
#             continue
#         if re.match(r'^(L series|EN|L \d+/\d+|ELI:|ISSN )', line):
#             continue
#         if re.match(r'^\(\s*\d+\s*\)$', line):
#             continue

#         line = re.sub(r'\(\s*\d+\s*\)', '', line)
#         line = re.sub(r'\s+', ' ', line).strip()

#         if not line:
#             continue
#         if re.match(r'^(Whereas:|CHAPTER|Article \d+|ANNEX|Section )', line, re.I):
#             if buffer:
#                 cleaned.append(buffer.strip())
#                 buffer = ""
#             cleaned.append("")       
#             cleaned.append(line)
#         else:
#             if buffer:
#                 buffer += " " + line
#             else:
#                 buffer = line


#     if buffer:
#         cleaned.append(buffer.strip())

#     while cleaned and cleaned[0] == "":
#         cleaned.pop(0)

#     text = "\n".join(cleaned)

#     with open(text_path,'w', encoding = 'utf-8') as f:
#         f.write(text)

#     print(f'successfully generated: {text_path} ({len(cleaned)} lines)')


# if __name__ == '__main__': 
#     os.makedirs('data/raw', exist_ok = True)
#     extract_text('data/raw/gdpr.html', 'data/raw/gdpr.txt')
#     extract_text('data/raw/ai_act.html', 'data/raw/ai_act.txt')




def extract_units(html_path: str, doc_name: str) -> list[dict]:
    """Parse EUR-Lex HTML into structured units (articles + recitals)."""
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # delete footers
    for note in soup.find_all(class_="oj-note"):
        note.decompose()

    units = []

    # extract articles
    article_tags = soup.find_all(class_="oj-ti-art")
    for art_tag in article_tags:
        # article number is usually in the text of the tag itself, e.g., "Article 1"
        art_label = art_tag.get_text(strip=True)
        art_num = re.sub(r"^Article\s+", "", art_label).strip()

        # title is usually in the next sibling tag with class "eli-title" or "oj-sti-art"
        title = ""
        next_el = art_tag.find_next_sibling()
        if next_el and next_el.get("class"):
            classes = " ".join(next_el.get("class", []))
            if "eli-title" in classes or "oj-sti-art" in classes:
                title = next_el.get_text(strip=True)

        # collect all paragraphs under this article, until the next article
        paragraphs = []
        cursor = next_el.find_next_sibling() if next_el else art_tag.find_next_sibling()
        while cursor:
            # stop if we reach the next article
            if cursor.get("class") and "oj-ti-art" in cursor.get("class", []):
                break
            text = cursor.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)
            cursor = cursor.find_next_sibling()

        full_text = "\n".join(paragraphs)

        units.append({
            "doc": doc_name,
            "kind": "article",
            "article": art_num,
            "title": title,
            "text": full_text,
        })

    # recitals are usually in the preamble, before the first article, and are numbered (1), (2), etc.
    whereas = soup.find(string=re.compile(r"Whereas", re.I))
    if whereas:
        # from the "Whereas" element, find the parent and then iterate over the next elements to collect recitals
        start = whereas.find_parent()
        for el in start.find_all_next(["div", "p"]):
            text = el.get_text(" ", strip=True)
            m = re.match(r"^\((\d+)\)\s*(.*)", text)
            if m:
                num = m.group(1)
                body = m.group(2).strip()
                units.append({
                    "doc": doc_name,
                    "kind": "recital",
                    "number": num,
                    "title": "",
                    "text": body,
                })
            # stop collecting recitals if we reach the first article
            if el.get("class") and "oj-ti-art" in el.get("class", []):
                break

    return units


def main():
    raw_dir = Path("data/raw")
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    jobs = [
        (raw_dir / "gdpr.html", "gdpr", out_dir / "gdpr.jsonl"),
        (raw_dir / "ai_act.html", "ai_act", out_dir / "ai_act.jsonl"),
    ]

    for html_path, doc_name, out_path in jobs:
        if not html_path.exists():
            print(f"the file does not exist: {html_path}")
            continue

        units = extract_units(str(html_path), doc_name)
        with open(out_path, "w", encoding="utf-8") as f:
            for u in units:
                f.write(json.dumps(u, ensure_ascii=False) + "\n")

        n_art = sum(1 for u in units if u["kind"] == "article")
        n_rec = sum(1 for u in units if u["kind"] == "recital")
        print(f"{doc_name}: {n_art} articles, {n_rec} recitals → {out_path}")


if __name__ == "__main__":
    main()