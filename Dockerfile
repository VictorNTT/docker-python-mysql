FROM python:3.7-alpine

## Define context
WORKDIR /code

## Define Env variables for a flask app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

## Run alpine linux
RUN pwd
RUN apk add --no-cache gcc musl-dev linux-headers

## Installation for python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## Open a port for the container to the outside
EXPOSE 5000

## Copy files to the WORKDIR
COPY src-py .
COPY config .

## Checking on 
RUN pwd
RUN ls -l

CMD ["flask", "run"]