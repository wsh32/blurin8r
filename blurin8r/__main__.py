import process

import argparse
import cv2
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blur out faces')
    parser.add_argument('img', type=str, help='File to blur')
    parser.add_argument('--classifier', type=str, help='Classifier xml file',
                        default='../cascades/haarcascade_frontalface_default.xml')
    parser.add_argument('--out', type=str, help='Output file')

    args = parser.parse_args()
    img = cv2.imread(args.img)
    faces = process.find_faces_haar(img, args.classifier)
    blurred_img = process.blur_faces(img, faces)

    # show image
    if args.out:
        cv2.imwrite(args.out, blurred_img)
    else:
        out = np.hstack((img, blurred_img))
        cv2.imshow('out', out)
        cv2.waitKey()
        cv2.destroyAllWindows()

