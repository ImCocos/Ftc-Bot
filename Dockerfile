FROM python:3.9
RUN pip install aiogram
WORKDIR /
COPY . .
EXPOSE 80
CMD [ "python3", "Main.py"]
