FROM python:3.11.0
WORKDIR Ftc-Bot/
COPY . .
RUN pip install pipreqs
RUN pipreqs Ftc-Bot/
RUN pip install -r requirements.txt
CMD ["python", "Main.py"]
CMD docker build -t my_image .
CMD docker run -p 8000:8000 my_image
EXPOSE 80/tcp
