from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "I love eating pizza.",
    "Pizza is my favorite food.",
    "The car is parked outside."
]

embeddings = model.encode(texts)

similarity = cosine_similarity(embeddings)

print(similarity)