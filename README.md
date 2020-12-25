## This is [**mipt.one**](https://mipt.one/) - webservice for MIPT students

<p align="center">
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</p>

### Backend (ansamble of Docker images with docker-compose):
 - **traefik** as a proxy to nginx with let's encrypt ssl by let's encrypt certs
 - **nginx** as a proxy to WSGI gunicorn
 - **gunicorn**

 - **Django** as a main handler
 - **aiogram** as telegram bot

 - **PostgreSQL** as database
 
### Frontend:
 - HTML/CSS with bootstrap 5
 - JS & JQuery

Hosted on vultr.com with pure Ubuntu 18.04 and Docker

> Check out the [post](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx) which helped a lot


#### A note on system managment

`free -h`

#### A note on docker volumes

- `docker system prune -a` to clear all used space by docker
- list through the `docker volume ls`
- identify through the `docker volume inspect volume_name`

Useful command that lets you identify dangling volumes:
- `docker volume ls -f dangling=true`



#### A note on symbolic links

- `ln -s /var/lib/docker/volumes/miptonedocker_static_volume /home/docker/mipt.one-docker`
- `ln -s /var/lib/docker/volumes/miptonedocker_media_volume /home/docker/mipt.one-docker`
