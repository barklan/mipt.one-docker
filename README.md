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

---

# TODO:
 - play with psq (send some queries)
 
 ```
 # something like this:
 docker-compose exec db psql --username=hello_django --dbname=hello_django_dev
 \l
 
 ```
 
 - physics control panel separate page (koryavov, solutions, and labs)
 - quote generator to the main page random every load on header
 - deploy a scraper to srv -> scrape something daily and add to a db through pipeline --> display database contents on user input
 - blog on django?
 - train a PyTorch model as a test & and upload to perform inference live?
 - community support in vk?
 - database sequrity


### A note on docker volumes

- list through the `docker volume ls`
- identify through the `docker volume inspect volume_name`

/var/lib/docker/volumes/miptonedocker_media_volume/_data/imgbank/8.51.jpg
