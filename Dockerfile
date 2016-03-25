FROM python:3.4.4-wheezy

MAINTAINER Seva Zhidkov

ADD /leonard /leonard

WORKDIR /leonard

RUN ls

RUN ls

ENTRYPOINT ['python', 'start.py', '--adapter telegram']
