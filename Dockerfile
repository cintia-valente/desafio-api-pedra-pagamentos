FROM python:3

WORKDIR /app

COPY src/requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

COPY scripts /scripts

CMD ["sh", "-c", "python /scripts/load_data.py && gunicorn --reload -b 0.0.0.0:5000 app:app"]

