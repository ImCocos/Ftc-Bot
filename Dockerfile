FROM python:3.8-slim-buster

WORKDIR /

RUN pip install sqlite3
RUN pip install aiogram

COPY . .

CMD [ "python3", "Main.py"]
