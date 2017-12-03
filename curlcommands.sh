#echo 'Enter IP: '
#read ip
ip=35.205.140.65

#Show all images
#curl -s -X GET -H 'Accept: application/json' http://$ip/images | python3 -mjson.tool

#Get all containers
#curl -s -X GET -H 'Accept: application/json' http://$ip/containers | python -mjson.tool

#Get all running containers
#curl -s -X GET -H 'Accept: application/json' http://$ip/containers?state=running | python -mjson.tool
#curl -s -X GET -H 'Accept: application/json' http://$ip/containers?state=running | python -mjson.tool

#//Delete Image based on ID
#curl -s -X DELETE -H 'Accept: application/json' http://$ip/images/17e0d61a6326 | python -mjson.tool

#//Delete container based on ID
#curl -s -X DELETE -H 'Accept: application/json' http://$ip/containers/138b0a13e745 | python -mjson.tool

#//Delete all images
#curl -s -X DELETE -H 'Accept: application/json' http://$ip/images | python -mjson.tool

#//Delete all containers
#curl -s -X DELETE -H 'Accept: application/json' http://$ip/containers/ | python -mjson.tool

#//Create docker container
#	curl -X POST -H 'Content-Type: application/json' http://$ip/containers -d '{"image": "docker-cms"}'
#    curl -X POST -H 'Content-Type: application/json' http://$ip/containers -d '{"image": "b14752a6590e"}'
#    curl -X POST -H 'Content-Type: application/json' http://$ip/containers -d '{"image": "b14752a6590e","publish":"8081:22"}'

#//Create docker image
#curl -H 'Accept: application/json' -F "file=@../Dockerfile" http://$ip/images

#Display logs
#curl -s -X GET -H 'Accept: application/json' http://$ip/container/af3006c006d1/logs | python -mjson.tool


#//Change state of container
#curl -X PATCH -H 'Content-Type: application/json' http://$ip/containers/c8c60e8e0f02 -d '{"state": "running"}'
#curl -X PATCH -H 'Content-Type: application/json' http://$ip/containers/138b0a13e745 -d '{"state": "stopped"}'


#//Change state of image
#curl -s -X PATCH -H 'Content-Type: application/json' http://$ip/images/17e0d61a6326 -d '{"tag": "test:4.0"}'


