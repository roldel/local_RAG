FROM python:alpine

# Install necessary packages
RUN apk add --no-cache curl


# Install ollama pip package
RUN pip install ollama requests django uvicorn

WORKDIR /code/django

#CMD ["python", "/code/django/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]