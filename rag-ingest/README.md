<!-- artifact
emoji: 🗂️
tasks: p2-w5-t4
stack: Python, Chroma, BGE, sentence-transformers
-->

# RAG Ingest: docs → chunk → embed → Chroma

The first **end-to-end ingestion run** — the point where the earlier drills
(parse, embed) become one pipeline that lands real documents in a searchable
vector store:

```
docs/*.md  →  CHUNK  →  EMBED (BGE, local)  →  STORE (Chroma, local disk)
                                                        │
                                              query ────┘  embed question → nearest chunks
```

Next week's Q&A step sits directly on top of this store.

## Local-only, by design

The source docs are **internal company documentation** (5 Flutter/mobile
engineering pages exported from Confluence). So nothing leaves the machine:

- **No hosted parser.** Confluence gives clean markdown directly, so we skip
  Marker/LlamaParse/unstructured — those are hosted APIs and would ship
  internal content to a third party. (The parser bake-off in `document-parsing`
  still stands; it's for *public* PDFs.)
- **BGE runs locally**, **Chroma persists to a local folder**.
- **`docs/` and `chroma/` are gitignored** — neither the content nor the vector
  store is ever committed.

## What Chroma is

A **vector database**: it stores each chunk's embedding and is fast at "given
this query vector, find the nearest stored vectors." It keeps three things per
chunk together — the **vector** (for search), the **original text** (so we can
show the passage), and **metadata** (source file + chunk index, for citations
later). Runs locally, no server or Docker.

## The pieces

- **Chunking** — pack paragraphs into ~1000-char windows with ~200-char
  overlap. Overlap keeps an idea that straddles a boundary retrievable from
  either chunk instead of being split in half. (Deliberately simple here;
  comparing chunking strategies is its own task.)
- **Embedding** — `BAAI/bge-base-en-v1.5`, local and free. Passages are embedded
  as-is; a query gets the BGE retrieval instruction prepended.
- **Storing** — one Chroma collection with cosine distance; re-running rebuilds
  it fresh so chunks don't duplicate.

## Run

```bash
# one-time: a Python 3.12 venv for the ML stack (torch has no 3.14 wheels),
# reused across tasks so torch installs once instead of per-run
uv venv .ml-venv --python 3.12
uv pip install --python .ml-venv sentence-transformers chromadb

# ingest every doc in docs/ into Chroma
.ml-venv/bin/python rag-ingest/ingest.py

# prove retrieval works — embed a question, get the nearest chunks
.ml-venv/bin/python rag-ingest/ingest.py "how do deep links get handled?"
.ml-venv/bin/python rag-ingest/ingest.py "how do we push an update without an app store release?"
```

The query step is the "it works" checkpoint: it doesn't answer the question yet
(that's the LLM step next week) — it just confirms the retrieved chunks are
actually relevant to what was asked.
