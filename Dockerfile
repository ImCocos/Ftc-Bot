FROM python:3.9

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 0

WORKDIR /

RUN pip install aiogram

COPY . .

EXPOSE 8080

CMD [ "python3", "Main.py"]

