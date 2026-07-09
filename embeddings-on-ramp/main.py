"""
Embeddings on-ramp — see embeddings + cosine similarity work, concretely.

An embedding turns text into a fixed-length vector (all-MiniLM-L6-v2 -> 384 numbers),
positioned so that similar *meanings* sit close together. Cosine similarity measures the
angle between two vectors: ~1 = same direction (alike), ~0 = unrelated.

We embed 20 sentences across 5 obvious topics and confirm the model groups them:
same-topic pairs score HIGH, cross-topic pairs score LOW — without us telling it the topics.

Runs 100% locally, no API key. First run downloads the model (~90 MB).
"""
from sentence_transformers import SentenceTransformer

# 5 topics x 4 sentences = 20. The topic labels are ONLY for our own scoring below —
# the model never sees them.
GROUPS = {
    "cooking":     ["I baked fresh sourdough this morning.",
                    "She simmered the tomato sauce for hours.",
                    "The recipe needs two cups of flour.",
                    "We grilled vegetables for dinner."],
    "weather":     ["A thunderstorm rolled in overnight.",
                    "It's sunny with a light breeze today.",
                    "Heavy snow is forecast this weekend.",
                    "The heatwave made the city unbearable."],
    "programming": ["I refactored the authentication module today.",
                    "The unit tests finally passed.",
                    "She deployed the API to production.",
                    "Merge the pull request after review."],
    "animals":     ["The cat curled up on the windowsill.",
                    "Dogs need a walk every day.",
                    "A flock of birds crossed the sky.",
                    "The puppy chewed my shoe again."],
    "finance":     ["Interest rates rose again this quarter.",
                    "He put his savings into an index fund.",
                    "The startup raised a seed round.",
                    "Inflation quietly eroded their savings."],
}

sentences, labels = [], []
for topic, group in GROUPS.items():
    for s in group:
        sentences.append(s)
        labels.append(topic)

print("Loading model (first run downloads ~90 MB)…")
model = SentenceTransformer("all-MiniLM-L6-v2")

emb = model.encode(sentences)                 # shape: (20, 384)
print(f"\nEmbedded {len(sentences)} sentences -> each is a vector of {emb.shape[1]} numbers.")

sims = model.similarity(emb, emb)             # (20, 20) cosine-similarity matrix

# --- 1) For 3 example sentences, show the closest + farthest others ---
print("\n=== Nearest & farthest by meaning ===")
for q in (0, 8, 16):  # one from cooking, programming, finance
    row = [(sims[q][j].item(), j) for j in range(len(sentences)) if j != q]
    row.sort(reverse=True)
    (best_s, best_j), (worst_s, worst_j) = row[0], row[-1]
    print(f"\n  “{sentences[q]}”  [{labels[q]}]")
    print(f"    most similar : {best_s:.2f}  “{sentences[best_j]}”  [{labels[best_j]}]")
    print(f"    least similar: {worst_s:.2f}  “{sentences[worst_j]}”  [{labels[worst_j]}]")

# --- 2) The proof: average same-topic vs different-topic similarity ---
intra, inter = [], []
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        (intra if labels[i] == labels[j] else inter).append(sims[i][j].item())

avg_intra = sum(intra) / len(intra)
avg_inter = sum(inter) / len(inter)
print("\n=== The proof ===")
print(f"  avg cosine, SAME topic     : {avg_intra:.3f}")
print(f"  avg cosine, DIFFERENT topic: {avg_inter:.3f}")
print(f"  gap                        : {avg_intra - avg_inter:+.3f}")
print("\n  " + ("PASS — similar meanings score higher than unrelated ones."
                if avg_intra > avg_inter else
                "unexpected — same-topic did not beat cross-topic."))
