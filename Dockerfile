FROM python:3.11.1

SHELL ["/bin/bash", "-c"]


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

EXPOSE 8000

WORKDIR /cycle_proj

RUN pip install --upgrade pip
RUN mkdir /cycle_proj/static && mkdir /cycle_proj/media

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron \
    openssh-client flake8 python3-venv python3-dev locales \
    postgresql postgresql-contrib nginx curl


COPY . .
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["gunicorn","-b","0.0.0.0:8001","core.wsgi:application"]

