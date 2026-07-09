<!-- artifact
emoji: 🧭
tasks: p2-w5-t8
stack: Python, sentence-transformers, PyTorch
-->

# Embeddings On-Ramp

Turns 20 sentences into vectors with `sentence-transformers` (all-MiniLM-L6-v2, runs locally, no API key) and uses **cosine similarity** to confirm the intuition behind every RAG system: text with similar *meaning* lands close together in vector space.

The 20 sentences span 5 topics (cooking, weather, programming, animals, finance). The model never sees the topic labels — yet same-topic pairs score high and cross-topic pairs score low. `main.py` prints, for a few sentences, their nearest and farthest neighbours, then proves it with the average same-topic vs different-topic cosine similarity.

## Concepts

- **Embedding** — a model maps any text to a fixed-length vector (here, 384 numbers), positioned by meaning.
- **Cosine similarity** — the cosine of the angle between two vectors: `~1` alike, `~0` unrelated, `<0` opposite. Length-independent, so it compares *direction* (meaning), not magnitude.
- This is the retrieval core of RAG: embed your documents, embed the query, return the highest-cosine chunks.

## Run

```bash
uv run --no-project --python 3.12 --with sentence-transformers python main.py
```

First run downloads the model (~90 MB). Expect same-topic cosine well above cross-topic (a clear positive gap).
