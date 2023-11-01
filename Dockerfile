FROM python:3.8-slim-bullseye
COPY . .
RUN apt update && apt install -y git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
