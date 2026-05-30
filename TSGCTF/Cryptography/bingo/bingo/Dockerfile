FROM python:3.12-slim@sha256:fa48eefe2146644c2308b909d6bb7651a768178f84fc9550dcd495e4d6d84d01

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -yqq socat
WORKDIR /home/user/

COPY requirements.txt /home/user/requirements.txt
RUN pip install -r requirements.txt
COPY ./server.py /home/user/server.py

CMD ["socat", "TCP-L:10961,fork,reuseaddr", "EXEC:'python server.py'"]
