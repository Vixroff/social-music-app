# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1 

EXPOSE 8000

# CMD ["python3", "manage.py", "migrate"]
# CMD ["python3", "manage.py", "runserver"]
CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver"]
