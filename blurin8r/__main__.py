import process
import server

import argparse
import cv2
import numpy as np

import sys


def blur_frame(img, net, settings):
    faces = process.find_faces_yolo(img, net)
    # faces = process.find_faces_haar(img, args.classifier)

    blurred_img = process.blur_faces(img, faces,
                                     max_area=settings['max_face_size'],
                                     blur_value=settings['blur_value'],
                                     blur_size=settings['blur_size'])
    return blurred_img



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blur out faces')
    parser.add_argument('--img', type=str, help='File to blur')
    parser.add_argument('--cam', type=int, help='Camera capture', default=0)
    parser.add_argument('--classifier', type=str, help='Classifier xml file',
                        default='./cascades/haarcascade_frontalface_default.xml')
    parser.add_argument('--out', type=str, help='Output file')
    parser.add_argument('--cfg', type=str, help='cfg file',
                        default='./cfg/face-yolov3-tiny.cfg')
    parser.add_argument('--weights', type=str, help='weights file',
                        default='./model-weights/face-yolov3-tiny_41000.weights')

    args = parser.parse_args()

    net = process.generate_yolo_net(args.cfg, args.weights)

    server.start_server()

    if args.img is not None:
        # If img is specified run on image
        img = cv2.imread(args.img)
        blurred_img = blur_frame(img, net, server.settings)

        # show image
        if args.out:
            cv2.imwrite(args.out, blurred_img)
        else:
            out = np.hstack((img, blurred_img))
            cv2.imshow('out', out)
            cv2.waitKey()
    else:
        # run on video by default
        cap = cv2.VideoCapture(args.cam)

        while True:
            ret, img = cap.read()
            blurred_img = blur_frame(img, net, server.settings)
            out = np.hstack((img, blurred_img))
            cv2.imshow('out', out)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        cap.release()
    cv2.destroyAllWindows()

