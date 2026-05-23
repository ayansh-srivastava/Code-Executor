FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY services/api_gateway/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
#TODO: Optimize by copying only necessary files

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["uvicorn", "services.api_gateway.main:app", "--host", "0.0.0.0", "--port", "8080"]