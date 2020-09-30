FROM python:3

ENV TZ America/Santiago

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app



CMD python app.py