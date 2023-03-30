CMD sudo docker ps
CMD sudo docker build -t local-image-id/Image_Name:latest . 
FROM python:3.11.0
WORKDIR Ftc-Bot/
COPY . .
RUN pip install pipreqs
RUN pipreqs /path/to/project
RUN pip install -r requirements.txt
CMD ["python", "Main.py"]
EXPOSE 80/tcp
