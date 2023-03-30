FROM python:3.8
WORKDIR /Ftc-Bot
COPY . .
RUN pip install -r requirements.txt
CMD Main.py
