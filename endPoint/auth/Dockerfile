FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk --update add bash

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app

CMD ["python3", "service/main.py"]