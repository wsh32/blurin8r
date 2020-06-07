import process

import argparse
import cv2
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blur out faces')
    parser.add_argument('--classifier', type=str, help='Classifier xml file',
                        default='../cascades/haarcascade_frontalface_default.xml')
    parser.add_argument('--out', type=str, help='Output file')
    parser.add_argument('--cfg', type=str, help='cfg file', default='./cfg/face-yolov3-tiny.cfg')
    parser.add_argument('--weights', type=str, help='weights file', default='./model-weights/face-yolov3-tiny_41000.weights')


    args = parser.parse_args()

    cap = cv2.VideoCapture(2)

    while True:
        ret, img = cap.read()
        net = process.generate_yolo_net(args.cfg, args.weights)
        faces = process.find_faces_yolo(img, net)


        # faces = process.find_faces_haar(img, args.classifier)
        blurred_img = process.blur_faces(img, faces)

        out = np.hstack((img, blurred_img))
        cv2.imshow('out', out)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

