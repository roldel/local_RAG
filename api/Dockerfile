FROM ollama/ollama

WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the start script into the container
COPY ollama_model_pull.sh /app/ollama_model_pull.sh

# Ensure the script is executable
RUN chmod +x /app/ollama_model_pull.sh

ENTRYPOINT ["/app/ollama_model_pull.sh"]