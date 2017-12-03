#!/bin/bash

docker build -t docker-cms .
docker image ls
docker run -d -p 80:5000 --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock --name cms docker-cms
docker ps
