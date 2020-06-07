FROM python:3.8-buster
# original:
# FROM python:3-buster

RUN pip install --upgrade pip

RUN apt-get update && \
    apg-get install -y \
      libsm6 libxext6 libxrender-dev \
      libv4l-dev