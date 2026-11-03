"""Tests for extract_text.py using small hand-written HTML.

The real EUR-Lex files are large and may change, so the tests use tiny mock pages that reproduce the
structures which caused bugs (duplicate recitals, swallowed paragraphs, chapter headings leaking in).
"""

from extract_text import extract_units

# Structure A: recital wrappers with ids, number and text in separate table cells.
HTML_WITH_IDS = """
<html><body>
<p class="oj-normal">Whereas:</p>
<div class="eli-subdivision" id="rct_1"><table><tr>
  <td><p class="oj-normal">(1)</p></td><td><p class="oj-normal">Recital one text.</p></td></tr></table></div>
<div class="eli-subdivision" id="rct_2"><table><tr>
  <td><p class="oj-normal">(2)</p></td><td><p class="oj-normal">Recital two text.</p></td></tr></table></div>
<div class="eli-subdivision" id="art_1">
  <p class="oj-ti-art">Article 1</p>
  <div class="eli-title"><p class="oj-sti-art">Subject-matter</p></div>
  <div id="001.001"><p class="oj-normal">1. Para A, see Article 6(1)(f).</p></div>
  <div id="001.002"><p class="oj-normal">2. Para B</p></div>
</div>
</body></html>
"""

# Structure B: no ids; wrapper div plus a number-only <p> (this produced 346 = 2 x 173 recitals).
HTML_NO_IDS = """
<html><body>
<p class="oj-normal">Whereas:</p>
<div><table><tr><td><p class="oj-normal">(1)</p></td><td><p class="oj-normal">Recital one text.</p></td></tr></table></div>
<div><table><tr><td><p class="oj-normal">(2)</p></td><td><p class="oj-normal">Recital two text.</p></td></tr></table></div>
<p class="oj-ti-art">Article 1</p>
<p class="oj-sti-art">Subject-matter</p>
<p class="oj-normal">1. Para A</p>
</body></html>
"""

# Structure C: flat articles; no subtitle on article 2; chapter heading and signature must not leak in.
HTML_FLAT = """
<html><body>
<p class="oj-ti-art">Article 1</p>
<p class="oj-sti-art">Title one</p>
<p class="oj-normal">1. Para A</p>
<p class="oj-ti-section-1">CHAPTER II</p>
<p class="oj-ti-art">Article 2</p>
<p class="oj-normal">1. Para B, directly after the heading</p>
<p class="oj-normal">2. Para C</p>
<p class="oj-signatory">Done at Brussels</p>
</body></html>
"""


def run(tmp_path, html):
    p = tmp_path / "x.html"
    p.write_text(html, encoding="utf-8")
    return extract_units(str(p), "mock")


def recitals(units):
    return [u for u in units if u["kind"] == "recital"]


def articles(units):
    return [u for u in units if u["kind"] == "article"]


def test_recitals_with_ids_no_duplicates(tmp_path):
    r = recitals(run(tmp_path, HTML_WITH_IDS))
    assert [u["number"] for u in r] == ["1", "2"]
    assert r[0]["text"] == "Recital one text."


def test_recitals_without_ids_no_duplicates_no_empty(tmp_path):
    r = recitals(run(tmp_path, HTML_NO_IDS))
    assert [u["number"] for u in r] == ["1", "2"]
    assert all(u["text"] for u in r)


def test_article_keeps_cross_reference(tmp_path):
    a = articles(run(tmp_path, HTML_WITH_IDS))[0]
    assert "Article 6(1)(f)" in a["text"]
    assert a["title"] == "Subject-matter"
    assert a["text"].count("\n") == 1  # two paragraphs


def test_article_without_subtitle_keeps_first_paragraph(tmp_path):
    a2 = articles(run(tmp_path, HTML_FLAT))[1]
    assert a2["title"] == ""
    assert "Para B" in a2["text"]


def test_chapter_heading_and_signature_do_not_leak(tmp_path):
    a1, a2 = articles(run(tmp_path, HTML_FLAT))
    assert "CHAPTER" not in a1["text"]
    assert "Brussels" not in a2["text"]
