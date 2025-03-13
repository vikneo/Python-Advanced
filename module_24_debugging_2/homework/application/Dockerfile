FROM python:3-alpine

ADD requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

ADD static/ /var/server/static
ADD templates/ /var/server/templates
ADD app.py/ /var/server/app.py

CMD python /var/server/app.py
