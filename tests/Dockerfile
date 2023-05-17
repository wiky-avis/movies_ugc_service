FROM --platform=linux/amd64 python:3.11-buster

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

COPY . .

RUN chmod +x tests/run.sh

ENTRYPOINT ["/opt/app/tests/run.sh"]
