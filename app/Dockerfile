FROM python:3.6-slim

RUN apt-get update && apt-get install -y bash libpq-dev gcc

COPY requirements.txt /app/requirements.txt

COPY country-comp/ /app/country-comp

WORKDIR /app

RUN pip install -r requirements.txt

USER nobody
