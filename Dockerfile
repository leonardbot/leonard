FROM python:3.4.4-wheezy

MAINTAINER Seva Zhidkov

ADD /leonard /leonard

WORKDIR /leonard

RUN pip install -r requirements.txt --upgrade

ENTRYPOINT ['python', 'start.py', '--adapter telegram']
