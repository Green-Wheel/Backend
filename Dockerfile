# This file is a template, and might need editing before it works on your project.
FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
RUN apk add --no-cache postgresql-libs && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN apk add --no-cache g++ snappy-dev && \
    pip install --no-cache-dir --ignore-installed python-snappy

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN rm .env

# For Django
ENTRYPOINT [ "./docker/entrypoint.sh" ]
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
