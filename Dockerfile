FROM python:3

ADD . /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 27017
CMD ["python", "src/main.py"]