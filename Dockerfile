FROM python:3

WORKDIR /app

COPY src/requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

ENV PYTHONPATH=/app/src:$PYTHONPATH

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8080

CMD ["sh", "-c", "echo $PORT && gunicorn --reload -b 0.0.0.0:$PORT app.app:app"]

