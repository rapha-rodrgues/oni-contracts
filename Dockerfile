FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV CONTRACTS_ENV=development
ENV CONTRACTS_SECRET_KEY="CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."
ENV CONTRACTS_DEBUG=true
ENV CONTRACTS_ALLOWED_HOSTS=*

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/