FROM python:3.8.5-slim-buster
LABEL maintainer=vmgabriel-quick

WORKDIR /usr/app

RUN pip3 install --upgrade pip setuptools wheel
COPY ./requirements.txt /usr/app/requirements.txt
RUN \
 apt-get update &&\ 
 apt-get install -y python3 python3-pip libpq-dev python-dev &&\ 
 python3 -m pip install -r requirements.txt 


COPY . /usr/app

