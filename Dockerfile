FROM ubuntu:22.04 AS base

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib ffmpeg libsm6 libxext6  -y -y
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /myprojects
COPY . /myprojects/
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv alienv --python=python3
RUN apt-get install gdal-bin libgdal-dev -y
RUN /bin/bash -c "source /myprojects/alienv/bin/activate && pip install -r requirements.txt && pip install gunicorn torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2"
COPY . .