#!/bin/bash

SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
fi

$SUDO modprobe -r v4l2loopback
$SUDO modprobe v4l2loopback devices=1 video_nr=20 card_label="blurin8r"
