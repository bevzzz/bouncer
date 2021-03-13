FROM python:3.8

WORKDIR /bouncer

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev

COPY . .

CMD ["python3", "server_main.py"]