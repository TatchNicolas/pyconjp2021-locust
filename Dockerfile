FROM python:3.9

WORKDIR /opt/pycon2021/

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install

COPY sample_app/ sample_app/

CMD ["uvicorn", "sample_app:app", "--port", "8000"]
