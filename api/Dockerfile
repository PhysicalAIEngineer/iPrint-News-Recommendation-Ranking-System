FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements-api.txt .
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements-api.txt

COPY api ./api

EXPOSE 8000

CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8000"]
