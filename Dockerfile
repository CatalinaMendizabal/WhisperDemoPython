FROM python:slim-bullseye
COPY . .
RUN mv -i /etc/apt/trusted.gpg.d/debian-archive-*.asc  /root/
RUN ln -s /usr/share/keyrings/debian-archive-* /etc/apt/trusted.gpg.d/
RUN apt update && apt install -y git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
