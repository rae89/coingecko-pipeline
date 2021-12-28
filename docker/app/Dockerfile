FROM python:3.9.1
RUN apt-get update && apt-get install -y cron
RUN mkdir /coin_gecko
COPY coingecko-crontab /etc/cron.d/coingecko-crontab
RUN chmod 0644 /etc/cron.d/coingecko-crontab
COPY requirements.txt /coin_gecko
COPY etlrun.sh /coin_gecko
COPY ./src /coin_gecko
WORKDIR /coin_gecko
RUN chmod u+x etlrun.sh
RUN chmod u+x coingecko/*.py
RUN pip install -r requirements.txt
RUN crontab /etc/cron.d/coingecko-crontab
RUN touch /var/log/cron.log
CMD printenv >> /etc/environment && cron && tail -f /var/log/cron.log