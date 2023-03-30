FROM python:3.8-slim-buster

WORKDIR /

RUN pip install pipreqs
RUN pipreqs /Ftc-Bot/

COPY . .

CMD [ "python3", "Main.py"]
