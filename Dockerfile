FROM python:3.5-slim
MAINTAINER NZT

WORKDIR /usr/scr/app/bot
COPY . .
RUN apt-get update && apt-get install -y openssl && pip install -r requirements.txt

ENV PYTHONPATH /usr/src/app/bot
CMD ["python", "-u", "configure.py"]
