from django.shortcuts import render

def intro(request):
    return render (request, 'core/intro.html')



from django.http import HttpResponse
from asgiref.sync import sync_to_async
from ollama import AsyncClient
from .forms import PromptForm

async def generate_view(request):
    response = None

    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            message = {'role': 'user', 'content': prompt}
            client = AsyncClient(host='http://rag_ollama_api:11434')

            try:
                # Collect responses from the async generator
                responses = [part async for part in await client.chat(model='llama3.2', messages=[message], stream=True)]
                # Combine the content of all responses
                response = ''.join(part['message']['content'] for part in responses)
            except Exception as e:
                response = f"An error occurred: {e}"
    else:
        form = PromptForm()

    return render(request, 'core/chat_template.html', {'form': form, 'response': response})



from django.http import StreamingHttpResponse
from ollama import AsyncClient
import asyncio

async def generate_response(prompt):
    message = {'role': 'user', 'content': prompt}
    client = AsyncClient(host='http://rag_ollama_api:11434')
    async for part in await client.chat(model='llama3.2', messages=[message], stream=True):
        yield f"data: {part['message']['content']}\n\n"

async def stream_chat_response(request):
    prompt = request.GET.get('prompt', '')
    response = StreamingHttpResponse(generate_response(prompt), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response



from .forms import TextInputForm
import ollama

def embed_view(request):
    embedding_result = None

    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            text_to_embed = form.cleaned_data["text"]
            # Initialize the Ollama client with the specified host
            client = ollama.Client(host='http://rag_ollama_api:11434')
            # Generate the embedding using the specified model
            response = client.embed(model='mxbai-embed-large', input=text_to_embed)
            # Extract the embedding vector from the response
            embedding_result = response.get('embeddings')
    else:
        form = TextInputForm()

    return render(request, "core/embed.html", {
        "form": form,
        "embedding": embedding_result,
    })




from django.shortcuts import redirect, get_object_or_404
from .models import Document
from .forms  import DocumentForm

def document_list(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("documents_list")
    else:
        form = DocumentForm()

    docs = Document.objects.order_by("-uploaded_at")
    return render(request, "core/document_list.html", {
        "form": form,
        "documents": docs,
    })

def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    # remove file from storage
    doc.file.delete(save=False)
    doc.delete()
    return redirect("documents_list")



# core/views.py
from .forms import SearchForm
from .chroma_client import collection
from .models import Document

def semantic_search(request):

    results = []
    documents = Document.objects.order_by("-uploaded_at")

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # 1) embed the query
            client = ollama.Client(host='http://rag_ollama_api:11434')
            resp = client.embed(model="mxbai-embed-large", input=query)
            emb = resp["embeddings"]
            # 2) find top-1 in ChromaDB
            docs = collection.query(
                query_embeddings=emb,
                n_results=1
            )["documents"][0]
            retrieved = docs[0]   # the text we stored
            # 3) generate final answer
            out = client.generate(
                model="llama3.2",
                prompt=f"Using this data: {retrieved}\nAnswer: {query}"
            )
            results = out["response"]
    else:
        form = SearchForm()

    return render(request, "core/semantic_search.html", {
        "form": form,
        "results": results,
        "documents": documents,
    })





from django.urls import reverse
from .forms import ChatMessageForm
from ollama import Client
from django.views.decorators.http import require_http_methods

OLLAMA_HOST = "http://rag_ollama_api:11434"

@require_http_methods(["GET", "POST"])
def chat_page(request):
    """
    A session‐backed, synchronous chat page. Each POST appends the user's
    message and Ollama's reply to request.session["chat_history"].
    """
    # Initialize the chat history in the session if needed
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    history = request.session["chat_history"]  # list of {"role":…, "content":…}

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data["message"].strip()
            if user_text:
                # 1) Append the new user message
                history.append({ "role": "user", "content": user_text })

                # 2) Call Ollama chat(...) on the entire history
                try:
                    client = Client(host=OLLAMA_HOST)
                    result = client.chat(
                        model="llama3.2",
                        messages=history,
                        stream=False
                    )
                    # ✂️ CORRECT EXTRACTION HERE ✂️
                    assistant_text = result["message"]["content"]
                except Exception as e:
                    assistant_text = f"[Error calling Ollama: {e}]"

                # 3) Append the assistant reply
                history.append({ "role": "assistant", "content": assistant_text })

                # 4) Save back into session
                request.session["chat_history"] = history
                request.session.modified = True

                # 5) Redirect to avoid re‐POST on refresh
                return redirect(reverse("chat_page"))
    else:
        form = ChatMessageForm()

    return render(request, "core/chat.html", {
        "form": form,
        "history": history,
    })