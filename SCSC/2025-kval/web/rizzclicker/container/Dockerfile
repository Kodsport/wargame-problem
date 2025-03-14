FROM python:3.11.4-slim-bullseye

RUN apt-get update && apt-get install -y cron

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pip install flask gunicorn pyjwt

# Clean keys every 30 minutes to avoid server explosion
RUN echo "*/30 * * * * rm -rf /app/keys && mkdir -p /app/keys" > /etc/cron.d/cleanup_keys
RUN chmod 0644 /etc/cron.d/cleanup_keys
RUN crontab /etc/cron.d/cleanup_keys

EXPOSE 5000
CMD service cron start && gunicorn -w 4 -b 0.0.0.0:5000 app:app