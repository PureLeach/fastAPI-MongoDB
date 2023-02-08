FROM python:3.9-slim-buster

RUN mkdir /database_service
WORKDIR /database_service
COPY ./database_service ./database_service/
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
