FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY sp14/ /app

WORKDIR /app

CMD ["python3", "manage.py", "add_db", "--path", "data/"]

WORKDIR /app

CMD ["gunicorn", "sp14.wsgi:application", "--bind", "0:8000"]

 
