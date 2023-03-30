FROM python:3.9
FROM nginx
COPY html /usr/share/nginx/html

WORKDIR /

RUN pip install aiogram

COPY . .

EXPOSE 8080

CMD [ "python3", "Main.py"]

