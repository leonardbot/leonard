FROM python:3.4.4-wheezy

MAINTAINER Seva Zhidkov

ADD . /leonard

WORKDIR /leonard

RUN pip3 install -r requirements.txt --upgrade

CMD python3 start.py --adapter $LEONARD_ADAPTER
