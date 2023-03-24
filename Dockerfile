# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.11-slim

EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app/

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
