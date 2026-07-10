<!-- artifact
emoji: 📐
tasks: p2-w5-t3
stack: Python, sentence-transformers, BGE
-->

# Embeddings: Quality vs Cost

The task was to compare **OpenAI text-embedding-3-small**, **Cohere Embed v4**,
and **BGE** on quality vs cost. OpenAI and Cohere are paid APIs — so the
hands-on measurement uses **BGE only** (free, runs locally), and the two paid
models are compared from their **published specs**. To make the quality/cost
tradeoff real, BGE is run at **three sizes** (small → base → large): a bigger
model should retrieve better but costs more in dimensions (storage), RAM, and
encode time.

## How "quality" is measured

Not vibes — a **retrieval eval**, the same shape MTEB uses. `main.py` holds a
small corpus of passages and a set of queries, each with one known-correct
("gold") passage. It embeds everything, ranks passages by cosine similarity to
each query, and scores:

- **Recall@1** — was the top-ranked passage the correct one?
- **MRR@10** — `1 / rank` of the correct passage, averaged (rewards ranking it high).

The queries are **paraphrased** (little word overlap with the gold passage) and
every topic has a **near-duplicate distractor**, so a model can't win by lexical
matching — it has to capture meaning. That's the whole point of an embedding.

## Run

```bash
# one-time: a Python 3.12 venv for the ML stack (torch has no 3.14 wheels)
uv venv .ml-venv --python 3.12
uv pip install --python .ml-venv sentence-transformers

# no API key; first run downloads the BGE models (~1.9 GB across the 3 sizes)
.ml-venv/bin/python embeddings-compare/main.py
.ml-venv/bin/python embeddings-compare/main.py small base
```

## Measured — BGE, locally ($0)

_10 paraphrased queries, 15 passages. Recall@1 and MRR@10 as defined above._

| model | dims | download | Recall@1 | MRR@10 |
|-------|-----:|---------:|---------:|-------:|
| bge-small  | 384  | ~0.13 GB | **0.90** | **0.950** |
| bge-base   | 768  | ~0.44 GB | **0.90** | **0.950** |
| bge-large  | 1024 | ~1.34 GB | **0.90** | **0.950** |

**All three tie** — same 9/10 correct, same MRR. That's the headline finding,
not a bug: on a clear-cut retrieval task the little 384-dim model is every bit
as good as the 1024-dim one. (Encode times at this scale — 25 short texts — are
sub-second and dominated by model warm-up, so they don't rank cleanly; the
honest cost signal is the **dimensions** and **download size** columns, not
milliseconds.) To pull the models apart you'd need a harder corpus — longer,
domain-dense passages where the extra dimensions actually earn their keep.

## Cited — the paid APIs, from published docs (not run here)

| model | dims | MTEB | price / 1M tok | context | hosting |
|-------|-----:|-----:|---------------:|--------:|---------|
| **BGE-large-en-v1.5** | 1024 | ~64.2 | **$0 (local)** | 512 | self-host |
| OpenAI text-embedding-3-small | 1536 (→256) | 62.26 | $0.02 | 8K | API only |
| Cohere Embed v4 | 1536 (256–1536) | ~66 | $0.12 | 128K | API only, multimodal |

## The quality-vs-cost picture

- **"Cost" isn't one number.** The paid models bill per token but need zero
  infra; BGE is free per query but you pay in the model download, RAM, and
  encode latency (and you host it). Dimensions are a hidden cost too —
  1536-d vectors are 4× the storage/RAM of BGE-small's 384-d in your vector DB.
- **BGE-large is remarkably close to the paid options on English retrieval**
  (MTEB ~64 vs ~62–66) for **$0/token**. For an English-only RAG prototype,
  local BGE is often the right first choice — no key, no per-query bill, data
  never leaves your machine.
- **Where the paid APIs earn their price:** Cohere Embed v4's 128K context and
  multimodal + multilingual support, and OpenAI's zero-infra convenience +
  Matryoshka dimension trimming. If you need long documents, images, or 100+
  languages, BGE-en won't cut it.
- **Within BGE, the size sweep is the lesson:** here all three sizes tied at
  0.90 Recall@1, so the extra dimensions of `bge-large` bought *nothing* on this
  task while costing ~4× the vector storage of `bge-small`. Bigger is not free
  and not automatically better — pick the smallest size that clears your Recall
  bar, and only reach for a larger one when a real eval shows it helps.

_Sources: [OpenAI embeddings](https://openai.com/index/new-embedding-models-and-api-updates/),
[Cohere Embed v4](https://docs.cohere.com/docs/cohere-embed),
[BGE on Hugging Face](https://huggingface.co/BAAI/bge-large-en-v1.5)._
