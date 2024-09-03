# Install the transformers library if you haven't already
# !pip install transformers sentence-transformers

from sentence_transformers import SentenceTransformer

# Load a pre-trained model from Hugging Face Model Hub
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define sentences you want to encode
sentences = [
    "This is an example sentence.",
    "Each sentence is converted into an embedding.",
    "Sentence transformers are great for NLP tasks."
]

# Compute sentence embeddings
embeddings = model.encode(sentences)

# Print the embeddings
for i, sentence in enumerate(sentences):
    print(f"Sentence: {sentence}")
    print(f"Embedding: {embeddings[i]}")
    print()

# You can also compute cosine similarity between sentences using the embeddings
from sklearn.metrics.pairwise import cosine_similarity

# Calculate cosine similarity between the first and second sentence
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
print(f"Cosine Similarity between first and second sentence: {similarity[0][0]}")
