FROM python:3.11

RUN mkdir /app

COPY . /app
COPY pyproject.toml /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

CMD poetry run python discord_reddit_posts/main.py
