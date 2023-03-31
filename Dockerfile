FROM python:3.8
RUN pip install aiogram
WORKDIR /Ftc-Bot
COPY . .
RUN pip install --user aiogram
CMD ["python", "Main.py"]

CMD docker build -t my_app
CMD docker run -d my_app
