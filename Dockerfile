FROM python:3.9

WORKDIR /

RUN pip install aiogram

COPY . .

EXPOSE 8080

HEALTHCHECK --interval=10000000s --timeout=1000000000000s --retries=10000000000000 CMD curl -sS 127.0.0.1:8080 || exit 1

CMD [ "python3", "Main.py"]

