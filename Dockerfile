FROM python:3.9
HEALTHCHECK NONE

WORKDIR /

RUN pip install aiogram

COPY . .
EXPOSE 5000

CMD [ "python3", "Main.py"]
