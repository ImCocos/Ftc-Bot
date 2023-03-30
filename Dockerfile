FROM python:3.8-slim-buster

WORKDIR /

RUN pip install aiogram

COPY . .
EXPOSE 8000

CMD [ "python3", "Main.py"]
