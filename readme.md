# Docker Compose Getting Started

## Prereq's

### Install Docker

    curl -fsSL get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo docker run hello-world
    sudo usermod -aG docker vcm
    sudo usermod -aG docker pi

### Docker Compose

    sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version

## Get and bring up the repo

    git clone git@gitlab.oit.duke.edu:dpb6/flask-redis-docker-compose-vm.git
    cd flask-redis-docker-compose-vm
    docker-compose up -d

## Test the routes

Go to the URL and port

- http://vcm-201.vm.duke.edu:5000
- http://localhost:5000

## Rebuild Docker Image after adding to requirements.txt

    sudo docker-compose build

## To Clean Up

Optionally use `--volumes` to delete the Redis data volume.

    docker-compose down --volumes
