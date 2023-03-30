FROM python:3.9

WORKDIR /

RUN pip install aiogram

COPY . .
EXPOSE 5000

CMD [ "python3", "Main.py"]

RUN docker container commit c16378f943fe rhel-httpd:latest
RUN docker image tag rhel-httpd:latest registry-host:5000/myadmin/rhel-httpd:latest
RUN docker image push registry-host:5000/myadmin/rhel-httpd:latest
