FROM python:3.9
RUN pip install aiogram
FROM nginx
COPY html /usr/share/nginx/html

CMD docker-compose up -d --build

WORKDIR /


COPY . .

EXPOSE 80

CMD [ "python3", "Main.py"]

