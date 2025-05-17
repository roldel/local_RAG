# core/chroma_client.py
import os
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from chromadb.errors import NotFoundError

# Where your Docker volume is mounted
CHROMA_DIR = os.environ.get("CHROMA_PERSIST_DIR", "/code/chroma")

# 1) Create a local, persistent client
client = chromadb.PersistentClient(
    path=CHROMA_DIR,
    settings=Settings(),            # default settings
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# 2) Get or create the collection
try:
    _collection = client.get_collection(name="documents")
except NotFoundError:
    _collection = client.create_collection(name="documents")
except Exception:
    _collection = client.create_collection(name="documents")

# Export both the client and the collection
collection = _collection
