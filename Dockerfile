FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc g++ python3-dev default-libmysqlclient-dev pkg-config pipenv && \
    rm -rf /var/lib/apt/lists/*
RUN pip install uwsgi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

#RUN python manage.py collectstatic --noinput
#RUN python manage.py loaddata users_fixture.json posts_fixture.json comments_fixture.json

EXPOSE 8000

#CMD ["sh", "-c", "python manage.py migrate && exec uwsgi --http-socket :8000 --module project_config.wsgi"]

