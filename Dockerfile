FROM python:3.9.13-slim-buster
COPY . .
RUN apt-get update && apt-get install -y git
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
