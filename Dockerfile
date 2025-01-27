FROM python:3

WORKDIR /app

COPY src/requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/

ENV PYTHONPATH=/app:$PYTHONPATH

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["sh", "-c", "python app/infrastructure/scripts/main.py && gunicorn --reload -b 0.0.0.0:8000 app.app:app"]

