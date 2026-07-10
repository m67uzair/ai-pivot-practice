"""
RAG ingestion pipeline (all local): docs -> chunk -> BGE embed -> Chroma.

This wires together the pieces from earlier tasks into one end-to-end run:
  parse (done upstream — here the docs are already clean markdown)
    -> CHUNK  (split into overlapping windows)
    -> EMBED  (BGE, the local/free embedder)
    -> STORE  (Chroma, a local on-disk vector database)

The source .md files are internal company docs exported into docs/. Nothing
leaves the machine: BGE runs locally and Chroma persists to a local folder.
Both docs/ and chroma/ are gitignored.

  ingest:  uv run --no-project --python 3.12 --with chromadb --with sentence-transformers python rag-ingest/ingest.py
  query:   uv run --no-project --python 3.12 --with chromadb --with sentence-transformers python rag-ingest/ingest.py "how do deep links work?"
"""
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).parent
DOCS = HERE / "docs"
CHROMA = HERE / "chroma"
COLLECTION = "linkedunion_docs"
MODEL = "BAAI/bge-base-en-v1.5"
# BGE wants this instruction prepended to the QUERY only (not to stored passages).
BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

CHUNK_SIZE = 1000     # characters per chunk (roughly)
CHUNK_OVERLAP = 200   # characters of tail carried into the next chunk


def chunk_text(text: str) -> list[str]:
    """Pack paragraphs into ~CHUNK_SIZE windows, overlapping by ~CHUNK_OVERLAP.

    Overlap matters: it keeps an idea that straddles a boundary retrievable from
    either chunk, instead of getting split in half and lost.
    """
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if cur and len(cur) + len(p) + 2 > CHUNK_SIZE:
            chunks.append(cur)
            cur = cur[-CHUNK_OVERLAP:] + "\n\n" + p  # carry a tail for context
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        chunks.append(cur)
    return chunks


def build() -> None:
    md_files = sorted(DOCS.glob("*.md"))
    if not md_files:
        print(f"No .md files in {DOCS} — export the Confluence pages there first.")
        return

    model = SentenceTransformer(MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA))
    # Rebuild fresh so re-running doesn't pile up duplicate chunks.
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    ids, docs, metas = [], [], []
    for f in md_files:
        chunks = chunk_text(f.read_text())
        for i, ch in enumerate(chunks):
            ids.append(f"{f.stem}::{i}")
            docs.append(ch)
            metas.append({"source": f.stem, "chunk": i})  # for citations later
        print(f"  {f.name:52} -> {len(chunks):>3} chunks")

    embeddings = model.encode(docs, normalize_embeddings=True).tolist()
    col.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)
    print(f"\nIngested {len(docs)} chunks from {len(md_files)} docs -> Chroma at {CHROMA}")
    print('Try:  ingest.py "how does screen tracking work?"')


def query(q: str, k: int = 4) -> None:
    model = SentenceTransformer(MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA))
    col = client.get_collection(COLLECTION)

    q_emb = model.encode([BGE_QUERY_INSTRUCTION + q], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=q_emb, n_results=k)

    print(f"\nQ: {q}\n")
    for rank, (doc, meta, dist) in enumerate(
        zip(res["documents"][0], res["metadatas"][0], res["distances"][0]), 1
    ):
        snippet = " ".join(doc.split())[:240]
        print(f"[{rank}] {meta['source']} (chunk {meta['chunk']})  cosine={1 - dist:.3f}")
        print(f"    {snippet}…\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query(" ".join(sys.argv[1:]))
    else:
        build()
