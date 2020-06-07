FROM python:3.8-buster
# original:
# FROM python:3-buster

# RUN pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y \
      libsm6 libxext6 libxrender-dev \
      libv4l-dev

WORKDIR /src
# COPY requirements.txt /src/
# RUN pip install --no-cache-dir -r /src/requirements.txt


#RUN sudo apt install v4l2loopback-dkms
#RUN sudo modprobe -r v4l2loopback
#RUN sudo modprobe v4l2loopback devices=1 video_nr=20 card_label='v4l2loopback' exclusive_caps=1

# Copy test images and actual code into new src docker working directory
# COPY test/ /src/
# COPY blurin8r /src/
# TODO: Probably need to add args to below line
# ENTRYPOINT python -u __main__.py
