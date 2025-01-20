import os
import shutil
from typing import List

import cv2
import numpy as np
import torch
from groundingdino.util.inference import load_image, predict, annotate
from groundingdino.util.inference import load_model
from torchvision.ops import box_convert


def copy_all_data():
    base_folder = '/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v2'
    dst_folder = '/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v2_see_all_in_one'

    for view in ["top", "side"]:
        for i in range(1, 41):
            src_file = os.path.join(base_folder, f"instance{i}/annotated_{view}_observation.png")

            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)

            dst_file = os.path.join(dst_folder, f"annotated_{view}_obj_{i}.png")
            shutil.copy(src_file, dst_file)
            print(f"Copied: {src_file} to {dst_file}")


class FindObjects:
    def __init__(self, is_save=True):
        # Get Visual Interpreter
        self.is_save = is_save
        self.model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
        self.gd_dir = os.path.join(self.model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.check_dir = os.path.join(self.model_dir, "weights/groundingdino_swint_ogc.pth")
        self.model = load_model(self.gd_dir, self.check_dir)
        self.BOX_THRESHOLD = 0.22
        self.TEXT_THRESHOLD = 0.22

        self.TEXT_PROMPT = ""
        self.detected_object = {}

    # Dinno
    def run_dinno(self, image_path):
        image_source, image = load_image(image_path=image_path)
        boxes, logits, phrases = predict(
            model=self.model,
            image=image,
            caption=self.TEXT_PROMPT,
            box_threshold=self.BOX_THRESHOLD,
            text_threshold=self.TEXT_THRESHOLD
        )
        labels = [
            f"{phrase} {logit:.2f}"
            for phrase, logit
            in zip(phrases, logits)
        ]

        # print(boxes)
        # print(phrases)

        h, w, _ = image_source.shape
        mask = (boxes[:, 2] <= 600 / w) | (boxes[:, 3] <= 300 / h)
        filtered_bb = boxes[mask]
        filtered_logits = logits[mask]

        annotated_frame = annotate(image_source=image_source, boxes=filtered_bb, logits=filtered_logits, phrases=phrases)
        return filtered_bb, phrases, annotated_frame

    def modifying_text_prompt(self, text_prompt: List):
        text_query = "".join([
            phrase + " ."
            for phrase in text_prompt
        ])
        self.TEXT_PROMPT = text_query

    def get_bbox(self, image_path, result_dir, is_save=True):
        boxes, phrases, frame = self.run_dinno(image_path)
        h, w, _ = frame.shape
        boxes = boxes * torch.Tensor([w, h, w, h])
        xyxy = box_convert(boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()

        for points, phrase, index in zip(xyxy, phrases, range(len(xyxy))):
            x1, y1, x2, y2 = points.astype(int)
            self.detected_object.update({index: {phrase: [int((x1 + x2) / 2), int((y1 + y2) / 2), x2 - x1, y2 - y1]}})

        return self.detected_object, frame


def main():
    # obj_num = 1
    # action_num = 0
    names = ["top_observation.png", "side_observation.png"]
    # names = ["side_observation.png"]

    for name in names:
        for i in range(1, 41):
            if i % 3 == 0:
                print("Current Index: ", i)
            image_path = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v2/instance{i}/" + name
            result_dir = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v2/instance{i}/"
            text_query = ["object"]

            detect_obj = FindObjects()
            detect_obj.modifying_text_prompt(text_query)
            detected_obj, anno_image = detect_obj.get_bbox(image_path, result_dir)
            cv2.imwrite(os.path.join(result_dir, f"annotated_{name}"), anno_image)


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


def cut_images():
    names = ["top_observation.png", "side_observation.png"]

    for name in names:
        for i in range(1, 46):
            image_path = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v2/instance{i}/" + name
            result_dir = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v2/instance{i}/"

            image = cv2.imread(image_path)
            # cv2.imshow("before", image)

            cropped_image = crop_image(image, [0, 0, 610, 480])
            # cv2.imshow("after", cropped_image)
            # cv2.waitKey(0)

            cv2.imwrite(image_path, cropped_image)


if __name__ == '__main__':
    copy_all_data()
