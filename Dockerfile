FROM python:3.7-alpine

ADD . /code
WORKDIR /code

RUN pip3 install -r requirements.txt

EXPOSE 27017
CMD ["python3", "src/main.py"]