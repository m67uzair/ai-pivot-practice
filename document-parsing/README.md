<!-- artifact
emoji: 📄
tasks: p2-w5-t2
stack: Python, httpx, LlamaParse, Marker (Datalab), unstructured, PyMuPDF
-->

# Document Parsing: LlamaParse vs Marker vs unstructured

Same PDF, three hosted parsers, output compared side-by-side. The goal was to
get a feel for how the leading "PDF → LLM-ready text" services actually behave
on a messy real document — a two-column academic paper with tables, inline
statistics, and multi-column author blocks.

## The test inputs

Both are the first 6 pages of the same arXiv paper (2607.05808, *"Say What?
Examining Text and Voice Input Modalities…"*), so the comparison is
apples-to-apples:

| File | How it's made | What it stresses |
|------|---------------|------------------|
| `pdfs/paper_6p.pdf`   | first 6 pages, untouched | layout / reading order (real text layer) |
| `pdfs/scanned_6p.pdf` | those pages rendered to JPEG images, no text layer | forces **OCR** — same content, so OCR quality is directly measurable |

Both PDFs are already generated and checked in. The scanned one was made by
rendering each page to a JPEG with PyMuPDF and wrapping it back into a PDF, so
it carries no text layer — the parsers *have* to OCR it.

## Run it

```bash
# keys in the repo-root .env: LLAMA_PARSE_API_KEY, MARKER_API_KEY, UNSTRUCTURED_API_KEY
uv run document-parsing/compare.py        # all three parsers × both inputs -> out/
uv run document-parsing/compare.py marker # or a subset
```

Each run writes `out/<parser>__<input>.md` and prints a timing/size summary.

## What to look for when comparing `out/`

Open the six files in `out/` and read them against the original PDF pages.
The interesting differences show up in a few specific places:

- **Tables.** The paper has two (a preference count table and a multi-header
  stats table). Did each parser emit real Markdown tables? Are the *numbers*
  correct and in the right cells, or are columns empty / shifted / merged
  wrong? Does one skip tables entirely?
- **Reading order.** It's a two-column layout with a multi-column author block.
  Did the text come out in sensible order, or did columns get interleaved?
  Are all authors + affiliations present and correctly paired?
- **Headings.** Which lines became `#` headings? Look for over-tagging (e.g.
  author names promoted to headings) vs. sensible section structure.
- **Hyphenation & spacing.** Words split across line breaks (`modal-\nity`) —
  rejoined cleanly, or left as `modal- ity`, or glued into `modality`? Any
  runs of words jammed together with no spaces?
- **Noise.** The arXiv vertical stamp down the left margin, page headers/
  footers, figure captions — kept, dropped, or garbled?
- **Born-digital vs. scanned.** Diff `<parser>__paper_6p.md` against
  `<parser>__scanned_6p.md` for the *same* parser. Since the content is
  identical, any difference is pure OCR cost. Which parser holds its structure
  best once there's no text layer to lean on?
- **Speed & output size.** `compare.py` prints seconds + char count per run.
  Note the spread — it's large.

Handy for spotting differences:

```bash
cd document-parsing/out
diff marker__paper_6p.md marker__scanned_6p.md   # OCR cost for one parser
grep -c '|' *.md                                  # rough table-row count
grep -cE '^#' *.md                                # heading count
```

### My findings

Judged by reading the six `out/` files against the original PDF pages
(speeds are measured by `compare.py`):

| | LlamaParse | unstructured | Marker (Datalab) |
|---|---|---|---|
| Speed (born / scanned) | 46s / 56s — slowest | 28s / 37s | **18s / 18s — fastest** |
| Reading order / columns | wrong alignment everywhere | somewhat better alignment | **correct order everywhere, columns intact** |
| Footer / running heads | not fully removed | not fully removed | **removed** |
| Text extracted from figures | none (even scanned) | none (even scanned) | **yes — pulled text out of figures** |
| Figures reconstructed | no | no | **yes — approximated figures as `---` layouts** |
| OCR (scanned) vs born-digital | slightly better alignment when scanned, still no figure text | same story — no figure text | held up |
| **Verdict** | weakest here | middle | **best — clear winner** |

**Bottom line: Marker wins on this document.** It kept two-column reading
order, stripped the footer, and was the only one to get *anything* out of the
figures — it even rebuilt figure structure from the extracted text using
Markdown rules. LlamaParse got alignment wrong throughout and pulled no figure
text; unstructured aligned somewhat better but still ignored the figures. And
Marker did all this while being ~2.5× faster than LlamaParse.

One thing worth knowing before you judge unstructured: it returns **typed
elements** (`Title`, `Table`, `NarrativeText`…), and `compare.py` flattens
them to plain text. Table structure isn't in the `.text` field — it lives in
each element's `metadata.text_as_html`. So "no tables in the output" may be a
flattening choice, not a parser limitation. Keep that in mind (or tweak
`parse_unstructured` to pull the HTML).

Outputs are checked in under `out/` so you can compare without re-running
(and re-spending API credits).
