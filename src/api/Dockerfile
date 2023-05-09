FROM --platform=linux/amd64 python:3.11-buster

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

# Нужно сюда вписать будет поетри установку
COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x run.sh

ENTRYPOINT ["/opt/app/run.sh"]
