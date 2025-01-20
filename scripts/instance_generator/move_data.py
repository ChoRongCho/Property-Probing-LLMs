import os
import shutil

import cv2
import numpy as np


def main():
    # 기본 폴더 경로 설정
    base_folder = '/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v2'
    side_prefix = 'capture_side_'
    top_prefix = 'capture_top_'

    # 하위 폴더 생성 및 파일 이동
    for i in range(1, 46):
        instance_folder = os.path.join(base_folder, f'instance{i}')
        os.makedirs(instance_folder, exist_ok=True)

        side_image = f'{side_prefix}{i}.png'
        top_image = f'{top_prefix}{i}.png'

        side_image_path = os.path.join(base_folder, side_image)
        top_image_path = os.path.join(base_folder, top_image)

        if os.path.exists(side_image_path) and os.path.exists(top_image_path):
            # shutil.move(side_image_path, os.path.join(instance_folder, side_image))
            # shutil.move(top_image_path, os.path.join(instance_folder, top_image))
            new_side_image_path = os.path.join(instance_folder, 'side_observation.png')
            new_top_image_path = os.path.join(instance_folder, 'top_observation.png')

            shutil.move(side_image_path, new_side_image_path)
            shutil.move(top_image_path, new_top_image_path)

        else:
            print(f"Image files for instance {i} are missing.")

    print("Images have been organized into subfolders.")


def divide_datasets():
    base_folder = '/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/datasets'

    for view in ["top", "side"]:
        for i in range(1, 41):
            src_file = os.path.join(base_folder, f"{view}_observation_{i}.png")
            dst_folder = f'/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3/instance{i}'

            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)

            dst_file = os.path.join(dst_folder, f"{view}_observation.png")
            shutil.copy(src_file, dst_file)
            print(f"Copied: {src_file} to {dst_file}")


def copy_all_data():
    base_folder = '/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3'
    dst_folder = '/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_see_all_in_one'

    for view in ["top", "side"]:
        for i in range(1, 39):
            src_file = os.path.join(base_folder, f"instance{i}/annotated_{view}_observation.png")

            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)

            dst_file = os.path.join(dst_folder, f"annotated_{view}_obj_{i}.png")
            shutil.copy(src_file, dst_file)
            print(f"Copied: {src_file} to {dst_file}")


def merge_data():
    dist_dir = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_see_all_in_one/"
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    for i in range(1, 39):
        source = f'/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3/instance{i}/'
        top_name = f"annotated_top_observation.png"
        side_name = f"annotated_side_observation.png"
        dist = f"annotated_instance{i}.png"

        top_image = cv2.imread(os.path.join(source, top_name))
        side_image = cv2.imread(os.path.join(source, side_name))
        merged = np.hstack((top_image, side_image))
        cv2.imwrite(os.path.join(dist_dir, dist), merged)


if __name__ == '__main__':
    # divide_datasets()
    merge_data()
