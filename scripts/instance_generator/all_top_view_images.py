import cv2
import numpy as np


def main():
    path = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/datasets_v3/planning_instances/obj_top_11_v3.png"
    image = cv2.imread(path)

    # rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    resized_image = cv2.resize(image, (640, 480))

    cv2.imwrite('/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/datasets_v3/planning_instances/obj_top_11_v2.png', resized_image)


if __name__ == '__main__':
    main()