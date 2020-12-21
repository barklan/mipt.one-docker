## This is a playground server... for now
`docker system prune -a` to clear all used space by docker

This is [**mipt.one**](https://mipt.one/) - info webservice for MIPT students

Now migrated from simple LAMP stack and static webpages with bits of php to this:

### Backend (ansamble of Docker images with docker-compose):
 - **traefik** as a proxy to nginx with let's encrypt ssl by let's encrypt certs
 - **nginx** as a proxy to WSGI gunicorn
 - **gunicorn**
 - **Django**
 - **PostgreSQL** as a database
 
### Frontend:
 - HTML/CSS with bootstrap 4
 - bits of JS & Jquery

Hosted on vultr.com with pure Ubuntu 18.04 and Docker

> Check out the [post](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx) which helped a lot


### A note on system managment

`free -h`

### A note on docker volumes

- list through the `docker volume ls`
- identify through the `docker volume inspect volume_name`

The new volume API adds a useful command that lets you identify dangling volumes:
> docker volume ls -f dangling=true



/var/lib/docker/volumes/miptonedocker_media_volume/_data/imgbank/8.51.jpg

### A note on symbolic links

ln -s /var/lib/docker/volumes/miptonedocker_static_volume/_data /home/docker/mipt.one-docker


---


## TODO:

[kanban](https://github.com/barklan/mipt.one-docker/projects/1)
 
- make a degree in antiplag


---


kewords:

moodle mipt, в помощь раздолбаю, викимипт