FROM python:3.6.9-alpine

WORKDIR /work

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

COPY crontab /etc/crontabs/root
