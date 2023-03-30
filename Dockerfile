FROM python:3.8-slim-buster

WORKDIR /

RUN pip install requirements.txt
COPY . .

CMD [ "python3", "Main.py"]
