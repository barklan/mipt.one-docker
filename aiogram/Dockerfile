# pull official base image
FROM python:3.8.3

# set work directory
WORKDIR /usr/src/aiogram
RUN mkdir /usr/src/aiogram/mediafiles/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install -y gcc python3-dev ufw

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
RUN chmod +x /usr/src/aiogram/entrypoint.sh
ENTRYPOINT ["/usr/src/aiogram/entrypoint.sh"]
