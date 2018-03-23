#! /bin/bash

docker pull registry.docker-cn.com/library/mongo:3.4.7
docker run -d --name=mongo registry.docker-cn.com/library/mongo:3.4.7

docker pull registry.docker-cn.com/vimagick/scrapyd
docker build -t architecture_spider .
docker run -d --name architecture -p 6800:6800 --link mongo architecture_spider

curl http://localhost:6800/schedule.json -d project=architecture_spider -d spider=idchina
