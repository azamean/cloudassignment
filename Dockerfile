# Set the base image
FROM python:3

# File Author / Maintainer
MAINTAINER MarcusOByrne

# install curl and docker
RUN apt-get install -y curl
RUN curl -fsSL https://get.docker.com/ | sh

# Update the sources list
RUN apt-get update

# Update the sources list
RUN apt-get -y upgrade

# Copy the application folder inside the container
ADD /app /app

# Get pip to download and install requirements:
RUN pip install -r /app/requirements.txt

# Expose listener port
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /app
# Set the default command to execute    
# when creating a new container
CMD python3 server.py
