FROM python:3.11-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]