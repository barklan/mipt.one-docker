# pull official base image
FROM python:3.8.3

# set work directory
WORKDIR /usr/src/aiogram

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install -y gcc python3-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
RUN chmod +x /usr/src/aiogram/entrypoint.sh
ENTRYPOINT ["/usr/src/aiogram/entrypoint.sh"]
