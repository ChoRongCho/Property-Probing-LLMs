import os.path

import cv2
import numpy as np


def crop_image(image_dir, xywh):
    # get image and image.shape (h, w, c)
    if type(image_dir) == str:
        images = cv2.imread(image_dir)
        real_h = images.shape[0]
        real_w = images.shape[1]
    elif type(image_dir) == np.ndarray:
        images = image_dir
        real_h = images.shape[0]
        real_w = images.shape[1]
    else:
        print("insert directory or numpy array")
        raise TypeError

    x = xywh[0]
    y = xywh[1]
    w = xywh[2]
    h = xywh[3]

    # rotate if h > w
    if real_h > real_w:
        images = cv2.rotate(images, cv2.ROTATE_90_COUNTERCLOCKWISE)
        real_h = images.shape[0]
        real_w = images.shape[1]
        pass

    if x + w > real_w:
        print("insert value under", real_w, image_dir)
        raise ValueError
    if y + h > real_h:
        print("insert value under", real_h, image_dir)
        raise ValueError

    # cropped_image = images[y: y + h, x: x + w, :]
    cropped_image = images[y: y + h, x: x + w]

    return cropped_image


def main():
    source = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_new"
    result = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_new_cropped"
    for i in range(1, 37):
        inst = f"instance{i}"
        os.makedirs(os.path.join(result, inst), exist_ok=True)
        # for name in ["side_observation.png", "top_observation.png"]:
        for name in ["side_observation.png"]:
            target_image = os.path.join(source, inst, name)
            image = cv2.imread(target_image)
            image = crop_image(image, [0, 0, 640, 480])
            # cv2.imshow("name", image)
            # cv2.waitKey(0)
            cv2.imwrite(os.path.join(result, inst, name), image)


if __name__ == '__main__':
    main()
