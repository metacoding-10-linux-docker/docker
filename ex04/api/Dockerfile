FROM python:3.10-alpine

WORKDIR /app

COPY app.py .

RUN pip install flask && pip install redis

CMD ["python", "app.py"]