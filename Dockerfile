FROM python:3.13-slim

ENV DJANGO_SETTINGS_MODULE=ratings-exercise.settings \
    PORT=8000

WORKDIR /app

RUN apt-get -y update \
    && apt-get -y upgrade

COPY . .

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN pip install -r requirements.txt

WORKDIR ratings-exercise

#CMD ["python manage.py migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]