FROM python:3.7.6

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY wehkamp-script.py /app
COPY secrets.py /app

CMD [ "python", "/app/wehkamp-script.py" ]