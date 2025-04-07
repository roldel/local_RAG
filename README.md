# local_RAG

**Local implementation of a minimalistic RAG application with its web interface**

local_RAG is a minimalistic Retrieval-Augmented Generation (RAG) application that provides a seamless web interface for interacting with a language model. The application uses Docker Compose to orchestrate a multi-container environment, integrating the Ollama project for document embedding, vector storage with ChromaDB, and language model processing, alongside a Django-powered web interface.

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
   - Manage a ChromaDB vector database for storing and retrieving embeddings.
   - Process user prompts through a language model, combining user input with relevant support documents.

2. **Web Service**  
   Runs on a Python:Alpine container and a Django application to:
   - Provide a user-friendly web interface.
   - Interact with the Ollama Service via the Ollama Python API and HTTP requests.
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
  - Integrates ChromaDB to manage embeddings.

- **Web Service**  
  - Runs on a Python:Alpine container.
  - Hosts a Django application that interacts with the Ollama Service.
  - Utilizes the Ollama Python API package for communication and processing.

---

## Requirements

- Docker & Docker Compose
- Git
- Initial nternet access (to pull required Docker images and required models)

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
  Once the containers are up and running, access the web interface by navigating to `http://localhost:<port>` (replace `<port>` with the configured port, typically defined in your Docker Compose file).

- **Submitting Prompts:**  
  Use the web interface to enter prompts. The Django application will forward your requests to the Ollama Service, which processes them and returns a response that integrates relevant support documents.

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

