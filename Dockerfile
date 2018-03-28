FROM registry.docker-cn.com/vimagick/scrapyd
RUN pip install pymongo supervisor -i 'https://mirrors.aliyun.com/pypi/simple/'

COPY . /architecture_spider/
RUN mkdir -p /architecture_spider/logs

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
