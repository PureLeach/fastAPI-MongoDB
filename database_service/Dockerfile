FROM python:3.8

RUN mkdir /database_service 
WORKDIR /database_service
COPY . /database_service
RUN pip install --no-cache-dir --upgrade -r requirements.txt
