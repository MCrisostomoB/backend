FROM python:3

ENV TZ America/Santiago

ADD / /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

CMD bash heroku-exec.sh && python app.py