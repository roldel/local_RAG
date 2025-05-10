from django.shortcuts import render

def intro(request):
    return render (request, 'core/intro.html')



from django.http import HttpResponse
from asgiref.sync import sync_to_async
from ollama import AsyncClient
from .forms import PromptForm

async def chat_view(request):
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
