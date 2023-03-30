FROM python:3.8-slim-buster

WORKDIR /

RUN pip install pipreqs
RUN pipreqs /Ftc-Bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "Main.py"]
