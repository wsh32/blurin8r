import cv2
import numpy as np


def find_faces_haar(img, classifier_filename, scale_factor=1.3, min_neighbors=5, debug=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    classifier = cv2.CascadeClassifier(classifier_filename)
    faces = classifier.detectMultiScale(gray, scale_factor, min_neighbors)
    return faces


def blur_faces(img, faces, max_area=None, debug=False):
    blur = cv2.blur(img, (25, 25))

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

