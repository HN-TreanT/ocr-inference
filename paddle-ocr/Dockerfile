FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN --no-cache pip install --upgrade pip \
    && pip install --no-cache-dir paddlepaddle \
    && pip install --no-cache-dir paddleocr
