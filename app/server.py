# Marcus O'Byrne C15519493
from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
import sys
import random
from tempfile import mkdtemp
from werkzeug import secure_filename
import hashlib


app = Flask(__name__)


@app.route('/')
def index():
    return """ Available API endpoints:
           <br> GET /containers                     List all containers
           <br> GET /containers?state=running       List running containers (only)
           <br> GET /containers/<id>                Inspect a specific container
           <br> GET /containers/<id>/logs           Dump specific container logs
           <br> GET /images                         List all images
           <br> POST /images                        Create a new image
           <br> POST /containers                    Create a new container
           <br> PATCH /containers/<id>              Change a container's state
           <br> PATCH /images/<id>                  Change a specific image's attributes
           <br> DELETE /containers/<id>             Delete a specific container
           <br> DELETE /containers                  Delete all containers (including running)
           <br> DELETE /images/<id>                 Delete a specific image
           <br> DELETE /images                      Delete all images """


# run docker commands in the shell
def docker(*args):

    cmd = ['docker']

    for sub in args:
        cmd.append(sub)

    process = Popen(cmd, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    error = stderr.decode('utf-8')
    out = stdout.decode('utf-8')

    if error.startswith('Error'):
        print('Error: {0} -> [1]'.format(' '.join(cmd), stderr))

    return error + out


# turn the output from "docker images" into a list
def docker_images_to_array(output):
    
    all = []

    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[2]
        each['tag'] = c[1]
        each['name'] = c[0]
        all.append(each)

    return all;


# turn the output form "docker ps" into a list
def docker_ps_to_array(output):

    all = []

    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['image'] = c[1]
        each['name'] = c[-1]
        each['ports'] = c[-2]
        all.append(each)

    return all


@app.route('/hello')
def hello():
    return 'hello'


#create image
@app.route('/images', methods=['POST'])
def images_create():

    """
    Create image (from uploaded Dockerfile)
    curl -H 'Accept: application/json' -F file=@Dockerfile http://localhost:8080/images
    dockerfile = request.files['file']
    dockerfile.save(secure_filename("Dockerfile"))
    #m = hashlib.md5()
    file_name = 'Dockerfile'
    #number = random.randint(1, 1000)
    #m.update (file_name.encode())
    #m.update (str(number).encode())
    folder_name = 'app'
    os.makedirs(folder_name)
    dockerfile.save (os.path.join(folder_name, file_name))
    # docker build -t docker-cms .
    docker ('build', '-t', folder_name, os.path.join(os.getcwd(), folder_name))
    print('docker build -t' + folder_name[0:12] + '' + os.path.join(os.getcwd(), folder_name))
    print(os.path.join (os.getcwd(), folder_name, file_name))
    print(os.getcwd())
    resp = 'File saved at: ' +  folder_name + ' and name:' + file_name
    return Response(response=resp, mimetype="application/json")
    """

    dockerfile = request.files['file']
    dirpath = mkdtemp()
    filename = secure_filename(dockerfile.filename)
    file_path = os.path.join(dirpath, filename)
    context_path = os.path.join(dirpath, '.')
    dockerfile.save(file_path)
    resp = docker('build', '-t', filename.lower(), '-f', file_path, context_path)
    return Response(response=resp, mimetype="application/json")


# create container
@app.route('/containers', methods=['POST'])
def containers_create():
    """
    Create container (from existing image using id or name)
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "my-app"}'
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e"}'
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e","publish":"8081:22"}'
    """
    body = request.get_json(force=True)
    image = body['image']

    if 'publish' in body:
        port = body['publish']
        id = docker('run', '-d', '-p', port, image)
    else:
        id = docker ('run', '-d', image)

    id = id[0:12]

    return Response(response='{"id": "%s"}' % id, mimetype="application/json")


# list all containers
@app.route('/containers', methods=['GET'])
def containers_index():

    if request.args.get('state') == 'running':
        output = docker('ps')
    else:
        output = docker('ps', '-a')

    resp = json.dumps(docker_ps_to_array(output))

    return Response(response=resp, mimetype="application/json")


# list all images
@app.route('/images', methods=['GET'])
def images_index():
    output = docker('images')
    resp = json.dumps(docker_images_to_array(output))
    return Response(response=resp, mimetype="application/json")


@app.route('/containers/<id>', methods=['PATCH'])
def containers_update(id):
    """
    Update container attributes (support: state=running|stopped)
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "running"}'
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "stopped"}'
    """

    body = request.get_json(force=True)
    
    try:
        state = body['state']
        if state == 'running':
            docker('restart', id)
        if state == 'stopped':
            docker('stop', id)
    except:
        pass

    resp = '{"id": "%s"}' % id

    return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
    """
    Update image attributes (support: name[:tag])  tag name should be lowercase only
    curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/7f2619ed1768 -d '{"tag": "test:1.0"}'
    """

    body = request.get_json(force=True)
    
    try:
        newTag = body['tag']
        docker ('tag', id, newTag)
    except:
        pass

    resp = '{"id": "%s"}' % id

    return Response(response=resp, mimetype="application/json")


@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
    """
    Delete a specific image
    curl -s -X DELETE -H 'Accept: application/json'
    http://localhost:8080/images/<id> | python -mjson.tool
    """

    docker ('rmi', id)
    resp = '{"id": "%s"}' % id

    return Response(response=resp, mimetype="application/json")


@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):
    """
    Delete a specific container - must be already stopped/killed
    curl -s -X DELETE -H 'Accept: application/json'
    http://localhost:8080/containers/<id> | python -mjson.tool
    """
    docker ('stop', id)
    docker ('rm', id)
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")


@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
    """
    Force remove all containers - dangrous!
    curl -X DELETE -H 'Accept: application/json'
    http://localhost:8080/containers
    """

    output = docker('ps', '-a')

    list = docker_ps_to_array(output)

    idS = []

    for c in list:
        id = c['id']
        docker('stop', id)
        docker('rm', id)
        idS.append(id)

    resp = json.dumps(idS)

    return Response(response=resp, mimetype="application/json")


@app.route('/images', methods=['DELETE'])
def images_remove_all():
    """
    Force remove all images - dangrous!
    curl -X DELETE -H 'Accept: application/json'
    http://localhost:8080/images
    """

    output = docker('images')

    list = docker_images_to_array(output)

    idS = []

    for c in list:
        id = c['id']
        docker('rmi', id)
        idS.append(id)

    resp = json.dumps(idS)

    return Response(response=resp, mimetype="application/json")


@app.route('/services', methods=['GET'])
def services_index():
    output = docker('service', 'ls')
    resp = json.dumps(docker_services_to_array(output))
    return Response(response=resp, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
        
