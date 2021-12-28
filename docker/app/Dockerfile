FROM python:3.9.1
RUN apt-get update && apt-get install -y cron
RUN mkdir /coingecko
COPY coingecko-crontab /etc/cron.d/coingecko-crontab
RUN chmod 0644 /etc/cron.d/coingecko-crontab
COPY requirements.txt /coingecko
COPY etlrun.sh /coingecko
COPY ./src /coingecko
WORKDIR /coingecko
RUN chmod u+x etlrun.sh
RUN chmod u+x coingecko/*.py
RUN pip install -r requirements.txt
RUN crontab /etc/cron.d/coingecko-crontab
RUN touch /var/log/cron.log
CMD printenv >> /etc/environment && cron && tail -f /var/log/cron.log