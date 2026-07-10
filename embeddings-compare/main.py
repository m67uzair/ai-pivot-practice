"""
Embeddings: quality vs cost.

The tracker task is "OpenAI text-embedding-3-small vs Cohere Embed v4 vs BGE".
OpenAI and Cohere are paid APIs, so the *hands-on* part uses BGE only — which is
free and runs locally — but across THREE sizes (small -> base -> large). That
size sweep is itself a quality-vs-cost curve: bigger model = better retrieval,
but more dimensions (storage), more RAM, and slower encoding.

"Quality" here is measured the way real embedding benchmarks (MTEB) measure it:
a retrieval eval. We have a small corpus of passages and a set of queries, each
with one known-correct passage. We embed everything, rank passages by cosine
similarity to each query, and score:
  - Recall@1 : did the #1 ranked passage match the gold answer?
  - MRR@10   : 1/rank of the gold answer, averaged (rewards ranking it high).

The queries are deliberately paraphrased (little word overlap with the gold
passage) and every domain has a near-duplicate distractor, so lexical matching
won't save a weak model — it has to understand meaning.

Run (no API key; first run downloads ~1.9 GB of models):
  uv venv .ml-venv --python 3.12 && uv pip install --python .ml-venv sentence-transformers
  .ml-venv/bin/python embeddings-compare/main.py
  .ml-venv/bin/python embeddings-compare/main.py small base
"""
import sys
import time

from sentence_transformers import SentenceTransformer

# BGE v1.5 wants an instruction on the QUERY (not the passages) for retrieval.
BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

# id -> passage. Same-domain pairs (p0/p1, p2/p3, …) are hard negatives for
# each other; p10–p14 are extra distractors with no matching query.
PASSAGES = {
    "p0":  "Pull the espresso shot for about 25 to 30 seconds until the crema turns golden.",
    "p1":  "Store roasted coffee beans in an airtight container away from light and heat.",
    "p2":  "A B-tree index speeds up lookups but slows down inserts, since the tree must stay balanced.",
    "p3":  "Adding an index to a rarely-queried column mostly wastes disk and write throughput.",
    "p4":  "Long slow runs on the weekend build the aerobic base a marathon demands.",
    "p5":  "Tapering your mileage in the final two weeks lets your legs recover before race day.",
    "p6":  "Most succulents rot if you water them again before the soil has fully dried out.",
    "p7":  "A south-facing window gives a fiddle-leaf fig the bright indirect light it prefers.",
    "p8":  "When central banks raise interest rates, monthly mortgage payments tend to climb.",
    "p9":  "A fixed-rate mortgage locks your repayment even if market rates jump later.",
    "p10": "Cold brew steeps coarse grounds in cold water for about twelve hours.",
    "p11": "A hash index gives constant-time equality lookups but cannot do range scans.",
    "p12": "Hill repeats develop the leg strength that flat running never really touches.",
    "p13": "Overwatering and poor drainage are the two most common killers of indoor plants.",
    "p14": "An adjustable-rate mortgage can reset to a much higher rate after the intro period.",
}

# query -> gold passage id. Phrased differently from the passage on purpose.
QUERIES = [
    ("How long should I brew a single shot of espresso?", "p0"),
    ("Best way to keep coffee fresh after it's roasted?", "p1"),
    ("Why does adding indexes make writing to a table slower?", "p2"),
    ("Is it worth indexing a column nobody ever filters on?", "p3"),
    ("What kind of running builds endurance for a marathon?", "p4"),
    ("Should I reduce how much I run right before the race?", "p5"),
    ("My cactus keeps going mushy — am I giving it too much water?", "p6"),
    ("Where in the house should I put my fiddle-leaf fig for light?", "p7"),
    ("Do rising interest rates increase what I pay on my home loan?", "p8"),
    ("How can I stop my mortgage payment from ever changing?", "p9"),
]

# name -> (hf_id, approx download size) for display only.
MODELS = {
    "small": ("BAAI/bge-small-en-v1.5", "~0.13 GB"),
    "base":  ("BAAI/bge-base-en-v1.5",  "~0.44 GB"),
    "large": ("BAAI/bge-large-en-v1.5", "~1.34 GB"),
}


def evaluate(name: str, hf_id: str, size: str) -> dict:
    model = SentenceTransformer(hf_id)

    passage_ids = list(PASSAGES)
    passage_texts = [PASSAGES[i] for i in passage_ids]
    query_texts = [BGE_QUERY_INSTRUCTION + q for q, _ in QUERIES]

    t0 = time.monotonic()
    p_emb = model.encode(passage_texts, normalize_embeddings=True)
    q_emb = model.encode(query_texts, normalize_embeddings=True)
    encode_s = time.monotonic() - t0

    sims = model.similarity(q_emb, p_emb)  # (Q x P) cosine, since normalized

    hits, rr = 0, 0.0
    for qi, (_, gold) in enumerate(QUERIES):
        ranked = sorted(range(len(passage_ids)), key=lambda pj: sims[qi][pj].item(), reverse=True)
        rank = next(r for r, pj in enumerate(ranked, 1) if passage_ids[pj] == gold)
        if rank == 1:
            hits += 1
        if rank <= 10:
            rr += 1.0 / rank

    n = len(QUERIES)
    return {
        "name": name,
        "dims": p_emb.shape[1],
        "size": size,
        "recall_at_1": hits / n,
        "mrr_at_10": rr / n,
        "encode_s": encode_s,
    }


def main() -> None:
    which = [a for a in sys.argv[1:] if a in MODELS] or list(MODELS)
    results = []
    for name in which:
        hf_id, size = MODELS[name]
        print(f"Loading bge-{name} ({hf_id}, {size} first-run download)…")
        results.append(evaluate(name, hf_id, size))

    print("\n=== BGE quality vs cost (measured locally, {} queries) ===".format(len(QUERIES)))
    print(f"{'model':10} {'dims':>5} {'download':>10} {'Recall@1':>9} {'MRR@10':>7} {'encode':>8}")
    for r in results:
        print(f"bge-{r['name']:6} {r['dims']:>5} {r['size']:>10} "
              f"{r['recall_at_1']:>9.2f} {r['mrr_at_10']:>7.3f} {r['encode_s']:>7.2f}s")

    print("\nRecall@1 = top-ranked passage was the correct one.  "
          "MRR@10 = 1/rank of the correct passage, averaged.")


if __name__ == "__main__":
    main()
