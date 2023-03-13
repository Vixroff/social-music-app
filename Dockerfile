# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.10

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000