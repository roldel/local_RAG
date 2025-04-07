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
