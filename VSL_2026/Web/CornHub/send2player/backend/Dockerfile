FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
COPY ./cornhub /cornhub

RUN mkdir -p /app/data &&\
    mkdir -p /home/appuser/logs &&\
    useradd -m appuser &&\
    chown -R appuser:appuser /app && \
    chown -R appuser:appuser /home/appuser/logs && \
    chmod -R 555 /app && \
    chmod 755 /app/data && \
    chmod 755 /home/appuser/logs

USER appuser

COPY flag_1.txt flag_2.txt /home/appuser/

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
