FROM python:3.9

WORKDIR /

RUN pip install aiogram

COPY . .
EXPOSE 5000

CMD [ "python3", "Main.py"]

RUN docker image push http://localhost:5000
