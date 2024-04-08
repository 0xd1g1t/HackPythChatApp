FROM python:3.11-alpine

RUN adduser --system flaskuser
RUN mkdir -p /srv/app

WORKDIR /srv/app

USER flaskuser

COPY ./requirements.txt /tmp/requirements.txt
COPY ./src /srv/app
RUN python3 -m pip install --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]