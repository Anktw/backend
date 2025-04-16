from python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . /app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]