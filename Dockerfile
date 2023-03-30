FROM python:3.9

WORKDIR /

RUN pip install aiogram

COPY . .
EXPOSE 8000

CMD [ "python3", "Main.py"]
