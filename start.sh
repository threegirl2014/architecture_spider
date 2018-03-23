docker pull registry.docker-cn.com/library/mongo:3.4.7
#docker pull registry.docker-cn.com/library/python:2.7.10
#docker build -t architecture_spider .
docker run -d --name=mongo registry.docker-cn.com/library/mongo:3.4.7
#docker run -d --name architecture -p 6800:6800 --link mongo architecture_spider

docker pull registry.docker-cn.com/vimagick/scrapyd
docker run -d --name scrapyd -p 6800:6800 registry.docker-cn.com/vimagick/scrapyd

curl http://localhost:6800/schedule.json -d project=architecture_spider -d spider=idchina
