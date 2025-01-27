FROM python:3

WORKDIR /app

COPY src/requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/

ENV PYTHONPATH=/app/src:$PYTHONPATH

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

ENV PORT 5000

CMD ["sh", "-c", "python app/infrastructure/scripts/main.py && gunicorn --reload -b 0.0.0.0:5000 app.app:app"]
