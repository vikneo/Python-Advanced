FROM python:3.9

RUN apt-get update && apt-get install -y python3-dev supervisor nginx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY hw_1/ /app/
COPY static/ /app/static/
COPY nginx.conf /etc/nginx/nginx.conf
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY supervisord.ini /etc/supervisor/conf.d/supervisord.ini


WORKDIR /app

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.ini"]
