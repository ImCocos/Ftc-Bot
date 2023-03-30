FROM python:3.9


WORKDIR /

RUN pip install aiogram

COPY . .

CMD [ "python3", "Main.py"]


FROM node
COPY server.js /
EXPOSE 8080 8081

HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl -sS 127.0.0.1:8080 || exit 1

CMD [ "node", "/server.js" ]

FROM node
 
COPY ..js /
 
EXPOSE 8080 8081
 
HEALTHCHECK --interval=5s --timeout= 10s --retries= 3 CMD curl -sS 127.0.0.1:8080 || exit 1
 
CMD [ "node", "/server.js" ]
. docker build . -t server:latest
# Lots, lots of output
CMD docker run -d --rm -p 8080:8080 -p 8081:8081 server
# ec36579aa452bf683cb17ee44cbab663d148f327be369821ec1df81b7a0e104b
CMD curl 127.0.0.1:8080
# OK

