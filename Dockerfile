FROM registry.docker-cn.com/vimagick/scrapyd
MAINTAINER rujiazhang@foxmail.com
RUN pip install pymongo supervisor -i 'https://mirrors.aliyun.com/pypi/simple/'
ENV LOGPATH /architecture_spider

WORKDIR /architecture_spider
ADD . /architecture_spider/
RUN mkdir -p /architecture_spider/logs

EXPOSE 6800

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENTRYPOINT ["supervisord"]
CMD ["-c", "/etc/supervisor/conf.d/supervisord.conf"]
