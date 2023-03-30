FROM python:3.8-slim-buster

WORKDIR /

RUN pip3 install pipreqs
RUN pip3 install pip-tools
RUN pipreqs --/Ftc-Bot=requirements.in && pip-compile
COPY . .

CMD [ "python3", "Main.py"]
