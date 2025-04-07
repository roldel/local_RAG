# Requirements & Planning for local_RAG

## Functional Requirements

### 1. Document Ingestion & Management
- **User Upload:**
  - Users must be able to upload, view, update, and delete their personal support documents via the web interface.
  - **Note:** In the initial implementation, support documents will be handled as plain text strings. Future iterations may support additional formats (e.g., PDFs, DOCX).
- **Embedding Generation:**
  - Uploaded documents are processed to generate vector embeddings using the **mxbai-embed-large** model.
  - The Django application calls the Ollama container via the Ollama Python package client to request these embeddings.
  - A Django **Document** model tracks and manages these documents (e.g., storing metadata such as title, creation date, and user ownership), while embeddings are stored in ChromaDB.

### 2. Retrieval-Augmented Generation (RAG) Pipeline
- **Prompt Embedding:**
  - Every time a user submits a prompt, the Django application sends a request to the Ollama container (through the Ollama Python package) to generate an embedding using **mxbai-embed-large**.
  - This prompt embedding is used to query ChromaDB for the most relevant documents.
- **Augmented LLM Processing:**
  - The original prompt, augmented with the retrieved document context, is sent to the Ollama container again—this time for LLM inference using the **llama3.2:3b** model.
  - The resulting response is returned to the user.

### 3. User Interface
- **Document Management Section:**
  - A dedicated section for users to manage their support documents (upload, view, update, delete).
  - Under the hood, these documents are stored via Django models and their embeddings in ChromaDB.
- **Prompt Submission Section:**
  - A user-friendly interface for entering prompts and displaying the final processed responses.

---

## Technical Requirements

### System Architecture
- **Multi-Container Deployment:**
  - Utilize Docker Compose to orchestrate:
    1. **Ollama Service Container:**  
       - Runs the official Ollama Docker image.
       - Performs all actual embedding (mxbai-embed-large) and LLM inference (llama3.2:3b) requests.
       - Exposes an API that the Python container can communicate with.
    2. **Web Service Container:**
       - Runs on a Python:Alpine image hosting a Django application.
       - Uses the Ollama Python package (a client library) to send embedding and inference requests to the Ollama container’s API.
       - Integrates **ChromaDB** for vector storage and retrieval, storing both document and prompt embeddings.
       - Manages user interactions (document uploads, prompt submissions) and stores document metadata in Django models.

### Dependencies
- **Core Technologies:**
  - Docker & Docker Compose
  - Git
- **Programming & Libraries:**
  - Python (Alpine) with Django
  - Django models to store document metadata (e.g., title, text content, upload date, user reference)
  - `requests` (potentially used for additional HTTP calls if needed)
  - **Ollama Python API package** (acts as a client to send requests to the Ollama container)
  - **ChromaDB Python library** (for vector storage and retrieval)

### API Endpoints
1. **Embedding Generation (Documents & Prompts):**
   - Handled by the Ollama container, invoked by the Django application through the Ollama Python package.
   - Uses **mxbai-embed-large** for all embedding requests.
   - Example: `ollama.embed(model="mxbai-embed-large", input="<text>")`
2. **LLM Inference:**
   - Also handled by the Ollama container, invoked by Django through the Ollama Python package.
   - Uses **llama3.2:3b** for final text generation.
   - Example: `ollama.generate(model="llama3.2:3b", prompt="<augmented-prompt>")`
3. **Document Management (Django):**
   - Endpoints for uploading, retrieving, updating, and deleting user documents.
   - Integrates with Django models to store document metadata, and uses ChromaDB to store/retrieve embeddings.

### Performance, Logging & Error Handling
- **Performance Expectations:**
  - Ensure minimal overhead between the prompt embedding, document retrieval, and final LLM processing steps.
  - Embedding (mxbai-embed-large) and LLM inference (llama3.2:3b) should respond within a few seconds under normal loads.
- **Logging & Monitoring:**
  - Log all major API calls (embedding requests, LLM requests, document operations) with sufficient detail.
  - Consider Docker’s built-in logging drivers or a centralized logging solution for easier aggregation and monitoring.
- **Error Handling & Resilience:**
  - Manage potential failures from the Ollama container gracefully (e.g., timeouts, unexpected API responses).
  - Validate user inputs to prevent crashes or malicious uploads.
  - Provide user-friendly error messages and maintain detailed error logs for debugging.

---

## User Flows

### Document Upload Flow
1. **Access Document Section:**  
   The user navigates to the document management area.
2. **Upload & Process:**  
   - The user uploads plain text documents.
   - Django uses the Ollama Python package to send an embedding request (`mxbai-embed-large`) to the Ollama container’s API.
   - The resulting embedding is stored in ChromaDB, while metadata is saved in Django’s database.
3. **Manage Documents:**  
   - The user can view, update, or delete previously uploaded documents.
   - Updates or deletions are reflected in both the Django database and ChromaDB.

### Prompt Submission Flow
1. **Enter Prompt:**  
   The user submits a prompt through the web interface.
2. **Prompt Embedding & Retrieval:**  
   - Django sends the prompt to the Ollama container (via the Ollama Python package) to generate an embedding (`mxbai-embed-large`).
   - The resulting prompt embedding is used to query ChromaDB for the most relevant user-uploaded documents.
3. **Augmented Processing:**  
   - The original prompt is augmented with the retrieved document context.
   - Django calls the Ollama container again to perform LLM inference (`llama3.2:3b`) on the augmented prompt.
4. **Display Response:**  
   The final response is presented to the user on the web interface.