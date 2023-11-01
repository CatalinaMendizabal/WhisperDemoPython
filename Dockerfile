FROM python:bullseye
COPY . .
RUN chmod 1777 /tmp
RUN apt update && apt install -y git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
