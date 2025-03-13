FROM python:3.7.9

WORKDIR /new_year_app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY new_year_application .

ENTRYPOINT ["python", "app.py"]
