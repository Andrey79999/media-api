FROM python:3.11-alpine

RUN pip install -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]