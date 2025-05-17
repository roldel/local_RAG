# core/signals.py

import os
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document
from .chroma_client import client, collection
import ollama

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Document)
def generate_embedding(sender, instance: Document, created, **kwargs):
    # Only run on new uploads
    if not created:
        return

    try:
        # 1) Read the uploaded file’s text
        #    (for PDFs/docs you’ll need an extractor like PyPDF2 or python-docx;
        #     here we assume plain-text uploads)
        file_path = instance.file.path
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            text = f.read()

        # 2) Call Ollama’s embedding API
        ollama_client = ollama.Client(host='http://rag_ollama_api:11434')
        resp = ollama_client.embed(
            model="mxbai-embed-large",
            input=text
        )
        embedding = resp["embeddings"]

        # 3) Store in ChromaDB under the Document’s PK
        collection.add(
            ids=[str(instance.pk)],
            embeddings=embedding,
            documents=[text],           # or store instance.file.url if you prefer
            metadatas=[{"filename": os.path.basename(file_path)}]
        )

        # 4) Persist to disk
        client.persist()

    except Exception as e:
        # Log but don’t re-raise—so uploads still succeed even if embedding fails
        logger.error(
            "Embedding failed for Document id=%s file=%s: %s",
            instance.pk,
            getattr(instance.file, 'name', '<unknown>'),
            e,
            exc_info=True
        )
