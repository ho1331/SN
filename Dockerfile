FROM python:3.10

COPY . /app

WORKDIR /app

RUN apt-get update && \
    pip install -r requirements.txt --no-cache-dir

EXPOSE 5000
