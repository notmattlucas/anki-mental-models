
FROM python:3.6

RUN mkdir -p /app/target

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app.py app.py

ENTRYPOINT ["python", "app.py"]
