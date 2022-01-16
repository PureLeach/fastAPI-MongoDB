FROM python:3.8


RUN mkdir /database_service 
COPY . /database_service
COPY requirements.txt /database_service 
WORKDIR /database_service


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 


RUN pip install --no-cache-dir --upgrade -r requirements.txt
