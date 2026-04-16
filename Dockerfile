FROM python:3.14.0-slim

ENV PYTHONUNBUFFERED=1

RUN apt update

RUN apt install gettext libpq5 -y

RUN mkdir /code

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .
RUN chmod 755 /code/deploy.sh

EXPOSE 8080

ENTRYPOINT [ "/code/deploy.sh" ]