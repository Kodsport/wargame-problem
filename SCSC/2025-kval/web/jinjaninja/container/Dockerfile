FROM python:3.11.4-slim-bullseye

# im feeling kind today ;)
RUN apt-get update && apt-get install -y curl wget

RUN mkdir /app
WORKDIR /app
COPY . .

RUN useradd user
RUN chmod -R  +rx /app

RUN pip install flask gunicorn

USER user

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]