FROM python:3.8.8

WORKDIR /app

# utc -> cts
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements /tmp/requirements
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r /tmp/requirements/prd.txt

CMD ["bash", "-c", "gunicorn -w 2 server.wsgi -b 0.0.0.0:80 --timeout 300"]