input='Llamas are members of the camelid family'


import ollama

# Initialize the Ollama client with the specified host
client = ollama.Client(host='http://rag_ollama_api:11434')

# Define the text to be embedded
text_to_embed = 'The sky is blue because of Rayleigh scattering'

# Generate the embedding using an appropriate model
response = client.embed(model='mxbai-embed-large', input=text_to_embed)

# Extract the embedding vector from the response
embedding = response['embeddings']

# Output the embedding vector
print(embedding)
