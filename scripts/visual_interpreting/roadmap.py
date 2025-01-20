import os

import cv2
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial import distance

from scripts.visual_interpreting.visual_interpreter import FindObjects


def compute_weighted_distance(pt1, pt2, img_width, img_height):
    weight_parameter = 0.9
    y_weight = ((pt1[1] + pt2[1]) / 2) / img_height
    x_weight = abs((img_width / 2) - ((pt1[0] + pt2[0]) / 2)) / (img_width / 2)
    return 1 + weight_parameter * y_weight + (1 - weight_parameter) * x_weight


def connect_mst(detected_obj, anno_image, im_h, im_w, name):
    centers = []
    for idx, bbox in detected_obj.items():
        cx, cy, w, h = bbox['object']
        centers.append((cx, cy))
    centers = np.array(centers, dtype=np.int32)
    dist_matrix = distance.cdist(centers, centers, 'euclidean')
    if "side" in name:
        for i in range(len(centers)):
            for j in range(len(centers)):
                if i != j:
                    pt1 = (int(centers[i][0]), int(centers[i][1]))
                    pt2 = (int(centers[j][0]), int(centers[j][1]))
                    weighted_distance = dist_matrix[i][j] * compute_weighted_distance(pt1, pt2, im_w, im_h)
                    dist_matrix[i][j] = weighted_distance
    mst = minimum_spanning_tree(dist_matrix).toarray()
    for i in range(len(centers)):
        for j in range(len(centers)):
            if mst[i, j] != 0:
                cv2.line(anno_image, (centers[i, 0], centers[i, 1]),
                         (centers[j, 0], centers[j, 1]), (255, 255, 255), 2)  # 파란색 선 그리기


def connect_line(detected_obj, anno_image, im_h, im_w, name):
    centers = []
    for idx, bbox in detected_obj.items():
        cx, cy, w, h = bbox['object']
        centers.append((cx, cy))

    dist_matrix = distance.cdist(centers, centers, 'euclidean')
    if "side" in name:
        for i in range(len(centers)):
            for j in range(len(centers)):
                if i != j:
                    pt1 = (int(centers[i][0]), int(centers[i][1]))
                    pt2 = (int(centers[j][0]), int(centers[j][1]))
                    weighted_distance = dist_matrix[i][j] * compute_weighted_distance(pt1, pt2, im_w, im_h)
                    dist_matrix[i][j] = weighted_distance

    for i in range(len(centers)):
        nearest_indices = np.argsort(dist_matrix[i])[1:4]
        closest_distance = dist_matrix[i][nearest_indices[1]]
        farthest_distance = dist_matrix[i][nearest_indices[-1]]
        for j in nearest_indices:
            pt1 = (int(centers[i][0]), int(centers[i][1]))
            pt2 = (int(centers[j][0]), int(centers[j][1]))
            if dist_matrix[i][j] <= 1.8 * closest_distance:
                cv2.line(anno_image, pt1, pt2, (255, 255, 255), 2)


def merge_data():
    dist_dir = ""
    source = ""
    top_name = ""
    side_name = ""
    dist = ""

    top_image = cv2.imread(os.path.join(source, top_name))
    side_image = cv2.imread(os.path.join(source, side_name))
    merged = np.hstack((top_image, side_image))
    cv2.imwrite(os.path.join(dist_dir, dist), merged)


