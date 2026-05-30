# Dockerfile for AliBaba Stream Cipher Challenge
FROM python:3.10-slim

# Metadata
LABEL maintainer="ctf-team"
LABEL challenge="AliBaba Game"

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir pycryptodome --break-system-packages

# Add challenge files
WORKDIR /chal
COPY alibaba_cave.py ./
COPY flag.txt ./

EXPOSE 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'python3 alibaba_cave.py',pty,stderr,setsid,sigint,sane