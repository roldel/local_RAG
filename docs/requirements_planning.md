# Requirements & Planning for local_RAG

This document outlines the functional and technical requirements, as well as the overall planning for the local_RAG project—a minimalistic retrieval-augmented generation (RAG) application with a web interface. The system leverages embedding models via the Ollama API, a vector database (ChromaDB) integrated within a Python:Alpine container running Django, and a multi-container orchestration setup using Docker Compose.

---

## Functional Requirements

### 1. Document Ingestion & Management
- **User Upload:**  
  Users must be able to upload, view, update, and delete their personal support documents via the web interface.
- **Embedding Generation:**  
  Uploaded documents are processed to generate vector embeddings using an embedding model (e.g., `mxbai-embed-large` via Ollama).

  **Note:** In the initial implementation, support documents will be handled as plain text strings to simplify the process of document ingestion, embedding, and retrieval. Future iterations may support additional formats such as PDFs, DOCX, or other media.


### 2. Retrieval-Augmented Generation (RAG) Pipeline
- **Prompt Embedding:**  
  When a user submits a prompt, the system generates an embedding for the prompt using the Ollama Service.
- **Context Retrieval:**  
  The generated prompt embedding is used to query the integrated ChromaDB within the Python container, retrieving the most relevant support documents.
- **Augmented LLM Processing:**  
  The original prompt, augmented with the retrieved context, is sent to the Ollama API for final LLM processing. The resulting response is then returned to the user.

### 3. User Interface
- **Document Management Section:**  
  A dedicated section for users to manage their support documents.
- **Prompt Submission Section:**  
  A user-friendly interface for entering prompts and displaying the final processed responses.

---

## Technical Requirements

### System Architecture
- **Multi-Container Deployment:**  
  Utilize Docker Compose to orchestrate:
  - **Ollama Service Container:**  
    Runs the official Ollama Docker image for embedding generation and LLM processing.
  - **Web Service Container:**  
    Runs on a Python:Alpine image hosting a Django application, which integrates:
    - **ChromaDB:** For vector storage and retrieval.
    - **Document Management & Prompt Processing:** For handling user interactions.
  
### Dependencies
- **Core Technologies:**  
  - Docker & Docker Compose  
  - Git
- **Programming & Libraries:**  
  - Python (Alpine) with Django  
  - `requests` for HTTP API calls  
  - Ollama Python API package  
  - ChromaDB Python library

### Performance & Scalability
- **Response Time:**  
  Ensure fast response times for:
  - Embedding generation
  - Vector retrieval from ChromaDB
  - LLM processing
- **Logging & Monitoring:**  
  Implement robust logging of API calls, errors, and system events. Plan for monitoring container performance.

### API Endpoints
- **APIs:**  
  - Endpoints for embedding generation (for both documents and prompts)
  - Endpoints for LLM processing  
  - Document management endpoints (upload, update, delete)

---

## User Flows

### Document Upload Flow
1. **Access Document Section:**  
   The user navigates to the document management area.
2. **Upload & Process:**  
   The user uploads support documents, which are then processed to generate and store vector embeddings in ChromaDB.
3. **Manage Documents:**  
   The user can view, update, or delete uploaded documents.

### Prompt Submission Flow
1. **Enter Prompt:**  
   The user submits a prompt through the web interface.
2. **Embedding & Retrieval:**  
   - The Django application sends the prompt to the Ollama Service to generate an embedding.
   - This embedding is used to query ChromaDB for the most relevant support documents.
3. **Augmented Processing:**  
   The original prompt is augmented with the retrieved context and sent back to the Ollama API for LLM processing.
4. **Display Response:**  
   The final response is presented to the user.
