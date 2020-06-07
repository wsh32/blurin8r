import process
import server

import argparse
import cv2
import numpy as np
import pyfakewebcam # generating fake webcam on top of v4l2loopback-utils
import os

from multiprocessing import Process, Queue


def blur_frame(img, net, settings):
    faces = process.find_faces_yolo(img, net)
    # faces = process.find_faces_haar(img, args.classifier)

    blurred_img = process.blur_faces(img, faces,
                                     max_area=settings['max_face_size'],
                                     blur_value=max(int(settings['blur_value']), 0),
                                     blur_size=settings['blur_size'])
    return blurred_img


def main(args, net, queue, debug=False):
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
        height, width = 720, 1280
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FPS, 60)

        try:
            fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height) # setup fake
        except FileNotFoundError:
            # Need to initialize
            os.system('./setup.sh')
            fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height) # setup fake

        while True:
            if queue.full():
                server.settings = queue.get()
            ret, img = cap.read()
            blurred_img = blur_frame(img, net, server.settings)
            blurred_img_rgb = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB) # switch BGR2RGB
            fake.schedule_frame(blurred_img_rgb)
            if debug:
                out = np.hstack((img, blurred_img))
                cv2.imshow('out', out)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break

        cap.release()
    cv2.destroyAllWindows()


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
    parser.add_argument('--debug', help='Enable debug mode', action='store_true')

    args = parser.parse_args()

    net = process.generate_yolo_net(args.cfg, args.weights)

    settings_queue = Queue(1)

    server_process = Process(target=server.start_server, args=(settings_queue, ))
    server_process.start()

    main_process = Process(target=main, args=(args, net, settings_queue, args.debug))
    main_process.start()
    main_process.join()