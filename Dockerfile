FROM python:3.9.1 as app
RUN apt-get update && apt-get install -y cron
RUN mkdir /coingecko
COPY ./app/coingecko-crontab /etc/cron.d/coingecko-crontab
RUN chmod 0644 /etc/cron.d/coingecko-crontab
COPY ./app/requirements.txt /coingecko
COPY ./app/etlrun.sh /coingecko
COPY ./app/src /coingecko
WORKDIR /coingecko
RUN chmod u+x etlrun.sh
RUN chmod u+x coingecko/*.py
RUN pip install -r requirements.txt
RUN crontab /etc/cron.d/coingecko-crontab
RUN touch /var/log/cron.log
CMD printenv >> /etc/environment && cron && tail -f /var/log/cron.log

FROM mysql:latest as db
COPY ./custom-mysql.cnf /etc/mysql/conf.d/