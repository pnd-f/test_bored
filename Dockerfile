FROM python:3.11.8-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bb
COPY . /bb/

RUN mkdir -p static && mkdir -p staticfiles
RUN pip install -r requirements.txt
RUN python3 manage.py collectstatic --noinput

EXPOSE 80
#CMD ["gunicorn", "src.wsgi:application", "-b", "0.0.0.0:8000"]
#ENTRYPOINT ["python", "manage.py", "migrate", "&&", "python", "manage.py", "runserver", "0.0.0.0:80"]
ENTRYPOINT exec sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:80"
