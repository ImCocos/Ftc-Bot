FROM python:3.11.0
WORKDIR Ftc-Bot/
COPY . .
pip install pipreqs
pipreqs /path/to/project
RUN pip install -r requirements.txt
CMD ["python", "Main.py"]
EXPOSE 80/tcp
