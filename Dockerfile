FROM python:3.10-alpine3.18

COPY requirements.txt /temp/requirements.txt
COPY application /application
WORKDIR /application
EXPOSE 8000

RUN apk add zlib-dev jpeg-dev gcc musl-dev

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user
