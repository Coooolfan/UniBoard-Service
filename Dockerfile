FROM python:3.12.4
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["python", "manage.py", "runserver","0.0.0.0:8000","--noreload"]