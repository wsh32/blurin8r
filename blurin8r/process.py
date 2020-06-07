import cv2
import numpy as np
from utils import *


def find_faces_haar(img, classifier_filename, scale_factor=1.3, min_neighbors=5, debug=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    classifier = cv2.CascadeClassifier(classifier_filename)
    faces = classifier.detectMultiScale(gray, scale_factor, min_neighbors)
    return faces


def generate_yolo_net(cfg, weights, debug=False):
    net = cv2.dnn.readNetFromDarknet(cfg, weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net


def find_faces_yolo(img, net, conf_threshold=CONF_THRESHOLD, nms_threshold=NMS_THRESHOLD):
    frame_height = img.shape[0]
    frame_width = img.shape[1]

    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                 [0, 0, 0], 1, crop=False)

    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(get_outputs_names(net))

    # filter by confidence and nms
    confidences = []
    boxes = []
    final_boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                width = int(detection[2] * frame_width)
                height = int(detection[3] * frame_height)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant
    # overlapping boxes with lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        final_boxes.append(box)
        left, top, right, bottom = refined_box(left, top, width, height)

    return final_boxes


def blur_faces(img, faces, max_area=None, debug=False):
    blur = cv2.blur(img, (50, 50))

    mask = np.zeros((np.size(img, 0), np.size(img, 1), np.size(img, 2)), dtype=np.uint8)
    for (x, y, w, h) in faces:
        if max_area is not None:
            if (w * h) > max_area:
                continue
        mask = cv2.rectangle(mask, (x, y), (x+w, y+h), (255, 255, 255), -1)

    out = np.where(mask==(255, 255, 255), blur, img)
    if debug:
        cv2.imshow('out', out)
        cv2.waitKey()
    return out

