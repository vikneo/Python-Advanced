FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /python_advanced

RUN pip install --upgrade pip "poetry==2.0.0"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY python_advanced .

CMD ["gunicorn", "", "--bind", "0.0.0.0:8000"]
