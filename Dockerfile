FROM python:3.7
MAINTAINER harumonia
WORKDIR /Project/daily_reporter
COPY ./requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
RUN mkdir -p /logs/gunicorn/
COPY . .
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]