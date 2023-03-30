FROM python:3.11.0
WORKDIR Ftc-Bot/
COPY . .
RUN pip install pipreqs
RUN pipreqs /
RUN pip install -r requirements.txt
EXPOSE 443
CMD ["python", "Main.py"]
CMD docker build -t my_image .
