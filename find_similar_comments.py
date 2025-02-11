import openai
import numpy as np

# Set your OpenAI API key
openai.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDQyNDZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.6sic8td7ZY-ky0LbdCniC8VvlTGCQ2jloiD9awQlANA"

# File paths
comments_file = "/data/comments.txt"
output_file = "/data/comments-similar.txt"

# Function to get embedding
def get_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Read comments from file
with open(comments_file, "r", encoding="utf-8") as f:
    comments = [line.strip() for line in f.readlines() if line.strip()]

# Generate embeddings
embeddings = [get_embedding(comment) for comment in comments]

# Compute cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

max_similarity = -1
similar_pair = ("", "")

for i in range(len(comments)):
    for j in range(i + 1, len(comments)):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        if sim > max_similarity:
            max_similarity = sim
            similar_pair = (comments[i], comments[j])

# Write the most similar pair to output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(similar_pair))

print("Most similar comments saved to", output_file)
