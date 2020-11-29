## This is a playground server... for now

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

TODO:
 - actually do something with the database
 - make a dynamic django page using templates
 - train a PyTorch model as a test & and upload to perform inference live