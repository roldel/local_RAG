# core/signals.py
import os, logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document
from .chroma_client import client, collection
import ollama

# PDF extractor
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Document)
def generate_embedding(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        file_path = instance.file.path
        # 1) Extract text
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            chunks = [p.extract_text() for p in reader.pages if p.extract_text()]
            text = "\n\n".join(chunks)
        else:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                text = f.read()

        # 2) Embed
        ollama_client = ollama.Client(host="http://rag_ollama_api:11434")
        resp = ollama_client.embed(model="mxbai-embed-large", input=text)
        embedding = resp["embeddings"]

        # 3) Store
        collection.add(
            ids=[str(instance.pk)],
            embeddings=embedding,
            documents=[text],
            metadatas=[{"filename": os.path.basename(file_path)}]
        )

        # 4) Persist
        client.persist()

    except Exception as e:
        logger.error(
            "Embedding failed for Document id=%s file=%s: %s",
            instance.pk,
            getattr(instance.file, "name", "<unknown>"),
            e,
            exc_info=True
        )
