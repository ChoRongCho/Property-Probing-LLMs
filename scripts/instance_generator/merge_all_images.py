import os
import re
from PIL import Image
import cv2
import numpy as np

BOX_SIZE = 70
X_OFFSET = 20
Y_OFFSET = 20
PATCH_H = 360
PATCH_W = 540


def insert_num(num, image):
    col = num % 7
    row = num // 7
    box_top_left = (col * PATCH_W + X_OFFSET, row * PATCH_H + Y_OFFSET)
    box_bot_right = (col * PATCH_W + X_OFFSET + BOX_SIZE, row * PATCH_H + Y_OFFSET + BOX_SIZE)
    # print(box_top_left, box_bot_right)
    cv2.rectangle(image, box_top_left, box_bot_right, (255, 255, 255), thickness=-1)  # 하얀 상자
    cv2.rectangle(image, box_top_left, box_bot_right, (0, 0, 0), thickness=2)  # 검은 테두리
    # add index
    index_text = str(num + 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2.0
    font_thickness = 5
    text_size = cv2.getTextSize(index_text, font, font_scale, font_thickness)[0]
    text_x = box_top_left[0] + (box_bot_right[0] - box_top_left[0] - text_size[0]) // 2
    text_y = box_top_left[1] + (box_bot_right[1] - box_top_left[1] + text_size[1]) // 2
    cv2.putText(image, index_text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness=font_thickness)


def adjust_brightness():
    ref_image = cv2.imread("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/datasets_v3/planning_instances/obj_top_11_origin.png")
    target_image = cv2.imread("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/datasets_v3/planning_instances/obj_top_11.png")

    hsv1 = cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)
    avg_brightness1 = hsv1[:, :, 2].mean()

    # 두 번째 이미지의 밝기 계산
    hsv2 = cv2.cvtColor(target_image, cv2.COLOR_BGR2HSV)
    avg_brightness2 = hsv2[:, :, 2].mean()

    # 밝기 조정 비율 계산
    adjustment_ratio = avg_brightness1 / avg_brightness2 * 0.9
    print(adjustment_ratio)

    # 두 번째 이미지의 V 채널 조정
    hsv2[:, :, 2] = np.clip(hsv2[:, :, 2] * adjustment_ratio, 0, 255).astype(np.uint8)

    # 조정된 이미지 다시 BGR로 변환
    adjusted_image = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)

    # 결과 이미지 보기
    cv2.imshow('Original Image 2', ref_image)
    cv2.imshow('Adjusted Image 2', adjusted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def get_images():
    filename = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/merged_objects_v3_2.png"
    image = cv2.imread(filename)
    for num in range(0, 14):
        insert_num(num, image)
    cv2.imshow('Image with Box', image)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    pil_image.save('/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/merged_objects_label_v5.pdf', "PDF")
    # cv2.imwrite('/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/merged_objects_label_v4.png', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def main():
    # 이미지 폴더 경로

    # names = ["top_observation.png", "side_observation.png"]
    # for name in names:
    image_files = []
    for i in range(1, 15):
        image_folder = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/datasets_v3/planning_instances"
        name = f"obj_top_{i}.png"
        image_files.append(os.path.join(image_folder, name))

    # 이미지 사이즈 설정
    img_width, img_height = 540, 360
    grid_height_size = 7
    grid_width_size = 2
    footnote_size = 60

    # 빈 캔버스 생성
    final_image = np.zeros((img_height * grid_width_size, img_width * grid_height_size, 3),
                           dtype=np.uint8)
    final_image.fill(255)

    for idx, file in enumerate(image_files):
        if idx >= grid_height_size * grid_width_size:
            break

        img = cv2.imread(file)
        img = cv2.resize(img, (img_width, img_height))

        row = idx // grid_height_size
        col = idx % grid_height_size

        y_offset = row * img_height
        final_image[y_offset:y_offset + img_height, col * img_width:(col + 1) * img_width] = img

        # 0:60

    output_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing",
                               'merged_objects_v3_2' + ".png")
    # output_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing", 'merged_all_objects_v3.png')
    cv2.imwrite(output_path, final_image)

    print(f"Combined image saved at {output_path}")

def all_top_view():
    # 이미지 폴더 경로

    # names = ["top_observation.png", "side_observation.png"]
    # for name in names:
    image_files = []
    for i in range(1, 39):
        image_folder = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3/instance{i}"
        name = f"top_observation.png"
        image_files.append(os.path.join(image_folder, name))

    # 이미지 사이즈 설정
    img_width, img_height = 240, 180
    grid_height_size = 8
    grid_width_size = 5
    footnote_size = 60

    # 빈 캔버스 생성
    final_image = np.zeros((img_height * grid_width_size, img_width * grid_height_size, 3),
                           dtype=np.uint8)
    final_image.fill(255)

    for idx, file in enumerate(image_files):
        if idx >= grid_height_size * grid_width_size:
            break

        img = cv2.imread(file)
        img = cv2.resize(img, (img_width, img_height))

        row = idx // grid_height_size
        col = idx % grid_height_size

        y_offset = row * img_height
        final_image[y_offset:y_offset + img_height, col * img_width:(col + 1) * img_width] = img

        # 0:60

    output_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing",
                               'all_instances' + ".png")
    # output_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing", 'merged_all_objects_v4.png')
    cv2.imwrite(output_path, final_image)

    print(f"Combined image saved at {output_path}")


if __name__ == '__main__':
    # all_top_view()
    # my_image = cv2.imread("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/all_instances.png")
    # for i in range(0, 38):
    #     insert_num(i, my_image)
    # cv2.imshow("Inserted", my_image)
    # cv2.waitKey(0)
    # cv2.imwrite("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/all_instances_numbering.png", my_image)
    get_images()
