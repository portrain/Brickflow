FROM python:latest

RUN apt-get update && apt-get install -y graphviz

RUN mkdir /app /data /output
WORKDIR /app

ADD ./requirements.txt /app
ADD ./brickflow.py /app
ADD ./core /app/core

RUN pip install --trusted-host pypi.python.org -r requirements.txt

VOLUME /app
VOLUME /data
VOLUME /output

ENV args --help

CMD ["sh", "-c", "python brickflow.py ${args}"]
