FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
COPY . .
RUN apt update && apt install -y git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
