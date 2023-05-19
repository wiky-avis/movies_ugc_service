FROM --platform=linux/amd64 python:3.11-buster

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

COPY pyproject.toml .

RUN pip3 install poetry==1.4.2 --no-cache-dir
RUN poetry config virtualenvs.create false && poetry install

COPY . .

RUN chmod +x src/run.sh

ENTRYPOINT ["/opt/app/src/run.sh"]
