FROM python:3.8
ARG VERBOSE=true
WORKDIR /Ftc-Bot
COPY . .
RUN pip install -r requirements.txt
CMD ["Python", "Main.py"]
