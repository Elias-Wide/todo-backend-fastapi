FROM python:3.12-slim

WORKDIR /backend

COPY requirements.txt .
 
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# Правильный формат (JSON array)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
