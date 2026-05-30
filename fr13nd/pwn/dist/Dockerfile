FROM ubuntu:22.04

RUN sed -i 's/^# deb/deb/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y python3.11 && apt-get install -y socat

WORKDIR /app

COPY server.py .
COPY flag.txt .

RUN useradd -m ctf
USER ctf

EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3.11 server.py"]
