FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /Demo

ADD . /Demo

COPY ./requirements.txt /Demo/requirements.txt

RUN pip install -r requirements.txt

COPY . /Demo

EXPOSE 8000