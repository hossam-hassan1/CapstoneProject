FROM python:3.8

RUN pip install --upgrade pip

WORKDIR /app/

ADD . /app/


RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]
