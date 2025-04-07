#!/bin/bash

# Start the Ollama server in the background
ollama serve &

# Capture the PID of the Ollama server process
OLLAMA_PID=$!

# Wait until the Ollama server is active
until curl -s http://localhost:11434/health > /dev/null; do
  sleep 1
done

# List of models to pull
models=("mxbai-embed-large" "llama3.2")

# Pull each model
for model in "${models[@]}"; do
  ollama pull "$model"
done

# Keep the Ollama server running
wait $OLLAMA_PID