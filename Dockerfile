FROM python:3.11-alpine

RUN adduser --system www-data
RUN mkdir -p /srv/app
RUN mkdir -p /srv/uploads
RUN chown www-data:www-data /srv/uploads

WORKDIR /srv/app

USER www-data

COPY ./requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]