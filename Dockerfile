# This file is a template, and might need editing before it works on your project.
FROM python:3.10-alpine

WORKDIR /tmp

RUN apk add curl gpg gpg-agent

#WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app
COPY docker/settings.py config/settings.py
RUN rm .env

# For Django
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
