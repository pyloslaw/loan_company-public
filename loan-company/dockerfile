# syntax=docker/dockerfile:1

#Build part
FROM python:3.10.8-slim AS builder
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

#venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


#Operational part
FROM python:3.10.8-slim

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*


COPY --from=builder /opt/venv /opt/venv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /loan_site
COPY . /loan_site/