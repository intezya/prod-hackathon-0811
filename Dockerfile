FROM python:3.12

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.8.3

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

ENV PYTHONPATH=/app

COPY ./alembic.ini /app/
COPY ./app /app/app

CMD [ "fastapi", "run", "app/main.py" ]