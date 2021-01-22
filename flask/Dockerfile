# pull official base image
FROM python:3.8.3

# set work directory
WORKDIR /home/app/flask
RUN mkdir /home/app/flask/mediafiles/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install -y gcc python3-dev ufw python3-opencv ca-certificates python3-dev git wget sudo ninja-build tesseract-ocr

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# this is for detection demo
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.7/index.html

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
RUN chmod +x /home/app/flask/entrypoint.sh
ENTRYPOINT ["/home/app/flask/entrypoint.sh"]