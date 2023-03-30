FROM python:3.9

WORKDIR /

RUN pip install aiogram

COPY . .

EXPOSE 8080

HEALTHCHECK --no-healthcheck

CMD [ "python3", "Main.py"]

