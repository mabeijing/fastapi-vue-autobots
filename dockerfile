FROM mabeijing/python3:1.0.0

WORKDIR /app


COPY . /app


CMD [ "gunicorn", "main:app", "-c", "gunicorn.conf.py" ]