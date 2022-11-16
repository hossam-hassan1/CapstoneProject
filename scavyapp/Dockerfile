FROM python:3.8

RUN pip install --upgrade pip

WORKDIR  /CapstoneProject/scavyapp/app/

ADD . /scavyapp/app/


RUN pip install -r requirements.txt

CMD ["uwsgi", "scavyapp/app/app.ini"]

# scavyapp/app/app.ini