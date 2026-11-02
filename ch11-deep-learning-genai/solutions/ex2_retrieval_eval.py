"""Exercise 11.2: more policy documents and a small evaluation of retrieval.

Each test question lists the document that should be retrieved. The hit rate tells
you how often the right document appears in the top 2: measure, don't guess.
"""
import numpy as np
from sentence_transformers import SentenceTransformer

docs = [
    "Orders above 500 MAD ship for free anywhere in Morocco.",
    "Refunds are processed within 7 business days after we receive the item.",
    "Customer support is open from 9:00 to 18:00, Monday to Saturday.",
    "Premium members get 10% off every order and priority delivery.",
    "Items can be returned within 30 days if they are unused and in their original packaging.",
    "We accept payment by card, by bank transfer and cash on delivery in major cities.",
    "Deliveries to Casablanca and Rabat arrive within 24 hours; other cities take 2 to 4 days.",
    "Gift cards are valid for one year and cannot be exchanged for cash.",
    "You can change your delivery address until the order has been shipped.",
    "Damaged items must be reported with a photo within 48 hours of delivery.",
    "Premium membership costs 99 MAD per year and can be cancelled at any time.",
    "Customers can track their parcel with the link sent by SMS after shipping.",
    "We do not ship to addresses outside Morocco at the moment.",
    "Invoices are available in your account under Orders, as PDF files.",
]
tests = [
    ("How long does a refund take?", 1),
    ("Do you deliver to France?", 12),
    ("Can I pay cash when the parcel arrives?", 5),
    ("My vase arrived broken, what should I do?", 9),
    ("How much is the premium subscription?", 10),
    ("When will my order reach Rabat?", 6),
    ("Where can I download my invoice?", 13),
]

embedder = SentenceTransformer("all-MiniLM-L6-v2")
doc_vectors = embedder.encode(docs, normalize_embeddings=True)

hits = 0
for question, expected in tests:
    scores = doc_vectors @ embedder.encode([question], normalize_embeddings=True)[0]
    top2 = list(np.argsort(scores)[::-1][:2])
    ok = expected in top2
    hits += ok
    print(f"{'OK  ' if ok else 'MISS'} {question}\n      -> {docs[top2[0]]}")

print(f"\nHit rate @2: {hits}/{len(tests)}")
print("Keep this test set. Re-run it whenever you change the embedding model, the"
      " chunking or the documents: it is your retrieval regression test.")
