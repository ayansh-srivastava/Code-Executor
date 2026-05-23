FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY services/code_execution/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

#TODO: Optimize by copying only necessary files
COPY . .

ENV PYTHONPATH=/app

EXPOSE 50051

CMD ["python", "services/code_execution/service.py"]