FROM python:3.4.4-wheezy

MAINTAINER Seva Zhidkov

ADD /leonard /leonard

RUN pip install -r /leonard/requirements.txt

WORKDIR /leonard

CMD ['python', 'start.py', '--adapter telegram']
