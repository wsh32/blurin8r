import process

import argparse
import cv2
import numpy as np

import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blur out faces')
    parser.add_argument('img', type=str, help='File to blur')
    parser.add_argument('--classifier', type=str, help='Classifier xml file',
                        default='../cascades/haarcascade_frontalface_default.xml')
    parser.add_argument('--out', type=str, help='Output file')
    parser.add_argument('--cfg', type=str, help='cfg file', default='./cfg/yolov3-face.cfg')
    parser.add_argument('--weights', type=str, help='weights file', default='./model-weights/yolov3-wider_16000.weights')

    args = parser.parse_args()
    img = cv2.imread(args.img)
    net = process.generate_yolo_net(args.cfg, args.weights)
    faces = process.find_faces_yolo(img, net)

    # faces = process.find_faces_haar(img, args.classifier)
    blurred_img = process.blur_faces(img, faces)

    # show image
    if args.out:
        cv2.imwrite(args.out, blurred_img)
    else:
        out = np.hstack((img, blurred_img))
        cv2.imshow('out', out)
        cv2.waitKey()
        cv2.destroyAllWindows()



