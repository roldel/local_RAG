# local_RAG

**Local implementation of a minimalistic RAG application with its web interface**

local_RAG is a minimalistic Retrieval-Augmented Generation (RAG) application that provides a seamless web interface for interacting with a language model. The application uses Docker Compose to orchestrate a multi-container environment, integrating the Ollama project for document embedding and language model processing alongside a Django-powered web interface that also manages the ChromaDB vector database for storing and retrieving embeddings.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

---

## Overview

local_RAG leverages two primary services:

1. **Ollama Service**  
   Uses the official Ollama Docker image to:
   - Convert support documents into embeddings.
   - Process user prompts through a language model, combining user input with relevant support documents.

2. **Web Service**  
   Runs on a Python:Alpine container and a Django application to:
   - Provide a user-friendly web interface.
   - Interact with the Ollama Service via the Ollama Python API and HTTP requests.
   - Integrate and manage the ChromaDB vector database for storing and retrieving embeddings.
   - Display processed responses to the user.

---

## Features

- **Document Embedding & Retrieval**: Transform support documents into embeddings and store them in a vector database.
- **LLM Processing**: Process user prompts using a language model enhanced with retrieved support documents.
- **User Interface**: A clean and intuitive Django-based web interface.
- **Containerized Deployment**: Utilizes Docker Compose for streamlined multi-container deployment.
- **Extensible Architecture**: Designed for future enhancements and additional features.

---

## Architecture

The project is divided into two main services:

- **Ollama Service**  
  - Runs on the official Ollama Docker image.
  - Exposes RESTful API endpoints for embedding conversion and LLM processing.

- **Web Service**  
  - Runs on a Python:Alpine container.
  - Hosts a Django application that interacts with the Ollama Service.
  - Integrates the ChromaDB vector database for managing embeddings.
  - Utilizes the Ollama Python API package for communication and processing.

---

## Requirements

- Docker & Docker Compose
- Git
- Internet access (to pull required Docker images and required models)
- Python dependencies including Django, requests, the Ollama Python API package, and the ChromaDB Python library

---

## Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/roldel/local_RAG.git
cd local_RAG
```

### Configure Environment Variables

- Create necessary environment variable files (e.g., `.env`) for both services.
- Define Django settings, API endpoints, and secrets in these files.
- Refer to the sample configuration files in the `/configs` directory.

### Docker Compose Setup

A `docker-compose.yml` file is provided to orchestrate both the Ollama and Web services. To build and start the containers, run:

```bash
docker-compose up --build
```

This command builds the images (if not already built) and starts both services.

---

## Usage

- **Accessing the Web Interface:**  
  Once the containers are up and running, open your browser and navigate to `http://localhost:<port>` (replace `<port>` with the port specified in your Docker Compose configuration).

- **Managing Your Documents:**  
  Use the Documents section of the web interface to upload and manage your personal support documents. These documents will be processed and embedded, making them available as context during prompt processing.

- **Submitting Prompts:**  
  Enter your prompt via the prompt submission section. The Django application first sends the prompt to the Ollama Service to generate an embedding. This embedding is then used within the Python container to retrieve relevant context from your uploaded documents via ChromaDB. Finally, the augmented prompt—combining your original input and the retrieved context—is sent back to the Ollama API for LLM processing, with the final response displayed on the web interface.


---

## Testing

- **Unit and Integration Tests:**  
  Tests are included for both Django views and API endpoints.
  
- **Running Tests:**  
  To run tests for the Django application, execute:

  ```bash
  docker-compose run web python manage.py test
  ```

---

## Roadmap

For a detailed project roadmap and task breakdown, please refer to the [Tasklist.md](./Tasklist.md) file. This file outlines all planned phases from initial setup to future enhancements.

---

## Contributing

Contributions are welcome! If you'd like to contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a pull request for review.

Please ensure your contributions follow the coding standards and include appropriate tests and documentation.
