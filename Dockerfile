FROM python:3.11-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/

RUN pip install -r /usr/src/app/requirements.txt
RUN pip install gunicorn

COPY . /usr/src/app/