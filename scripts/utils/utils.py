import argparse
import csv
import os.path

import cv2
import numpy as np


def parse_args_v2():
    parser = argparse.ArgumentParser()

    # task setting
    parser.add_argument("--task_name", type=str or int, default=None, help="domain name")
    parser.add_argument("--exp_name", type=int, default=None, help="experiment name 1, 2, ..., 36")
    parser.add_argument("--exp_number", type=int, default=0, help="experiment number for result1, result2")
    parser.add_argument("--is_save", type=int, default=1, help="save the response")
    parser.add_argument("--is_random", type=int, default=0, help="save the response")

    # experiment setting
    parser.add_argument("--max_predicates", type=int, default=1, help="number of predicates you want to generate")
    parser.add_argument("--use_database", type=bool, default=True, help="use exist database")

    # additional path
    parser.add_argument("--data_dir", type=str, default="data", help="")
    parser.add_argument("--json_dir", type=str, default="data/json", help="")
    parser.add_argument("--result_dir", type=str, default="result_naive_planning", help="")

    # json_dir
    parser.add_argument("--api_json", type=str, default=None, help="")
    parser.add_argument("--robot_json", type=str, default=None, help="")

    # related to problem generation and refinement
    parser.add_argument("--mkdb", type=bool, default=False, help="make database")
    parser.add_argument("--max_feedback", type=int, default=1, help="number of max replanning")
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    parser.add_argument("--image_version", type=int, default=1, help="image version")

    args = parser.parse_args()
    return args


def object_parsing(answer):
    objects_out_box = []
    objects_in_box = []
    bin_content = ""

    lines = answer.split('\n')
    for line in lines:
        if line.startswith("object out box:" or " object out box:"):
            objects_out_box = line.split(": ")[1].split(", ")
        elif line.startswith("object in box:" or " object in box:"):
            objects_in_box = line.split(": ")[1].split(", ")
        elif line.startswith("box:" or " box:"):
            bin_content = line.split(": ")[1].split(", ")
        elif line.startswith("object:"):
            objects_out_box = line.split(": ")[1].split(", ")

    objects_out_box = [obj for obj in objects_out_box if obj]
    objects_in_box = [obj for obj in objects_in_box if obj]
    bin_content = [obj for obj in bin_content if obj]

    unique_objects = list(set(objects_out_box + objects_in_box + bin_content))
    unique_objects = ', '.join(unique_objects)
    unique_objects = unique_objects.replace('_', ' ')
    unique_objects = [unique_objects]

    output_dict = {
        "Objects_out_box": objects_out_box,
        "Objects_in_box": objects_in_box,
        "Bin": bin_content
    }

    return output_dict, unique_objects

def parse_single_name(answer):
    lines = answer.split('\n')
    objects_out_box = []
    for line in lines:
        if line.startswith("object:"):
            objects_out_box = line.split(": ")[1].split(", ")

    objects_out_box = [obj for obj in objects_out_box if obj]
    output_dict = {
        "Object": objects_out_box
    }
    return output_dict


def merge_image(name, image_dir):
    images = []
    before_after = [0, 1]
    actions = ["push", "pull", "fold"]
    for at in actions:
        for ba in before_after:
            image_name = f"{name}_{at}_{ba}.png"
            image_path = os.path.join(image_dir, image_name)
            image = cv2.imread(image_path)
            print(image.shape)
            images.append(image)
    image1 = np.concatenate([images[0], images[1]], axis=0)
    image2 = np.concatenate([images[2], images[3]], axis=0)
    image3 = np.concatenate([images[4], images[5]], axis=0)
    total_image = np.concatenate([image1, image2, image3], axis=1)
    h, w, _ = total_image.shape
    all_new_image = cv2.resize(total_image, (w // 2, h // 2))
    cv2.line(all_new_image, (320 - 1, 0), (320 - 1, 480), color=(0, 0, 255), thickness=3)
    cv2.line(all_new_image, (640 - 1, 0), (640 - 1, 480), color=(0, 0, 255), thickness=3)
    cv2.imshow("asdf", all_new_image)

    save_dir = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/predicates_prove"
    save_name = os.path.join(save_dir, f"{name}.png")
    cv2.imwrite(save_name, all_new_image)
    cv2.waitKey(0)


def int_to_ordinal(n):
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = suffixes.get(n % 10, 'th')
    return str(n) + suffix


def list_file(directory):
    entries = os.listdir(directory)
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
    return files


def sort_files(file_list):
    keyword_order = {
        'top': 0,
        'side': 1,
        '1': 2,
        '2': 3,
        '3': 4
    }

    def get_keyword(file_name):
        for keyword in keyword_order:
            if keyword in file_name:
                return keyword_order[keyword], file_name
        return len(keyword_order), file_name

    # 파일 목록 정렬
    sorted_files = sorted(file_list, key=get_keyword)
    return sorted_files


def subdir_list(folder_path):
    all_list = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            if "obj" in item_path:
                all_list.append(item_path)
    return all_list


def dict_parsing(input_dict):
    output_dict = {}
    index = 0

    # Define a helper function to extract attributes from the object name
    def extract_attributes(obj_name):
        color, shape = obj_name.split('_', 1)
        return color, shape

    # Process Objects_out_box
    for obj_name in input_dict.get('Objects_out_box', []):
        color, shape = extract_attributes(obj_name)
        output_dict[index] = {
            "name": obj_name,
            "shape": shape,
            "color": color,
            "predicates": [],
            "init_pose": "out_box"
        }
        index += 1

    # Process Objects_in_box
    for obj_name in input_dict.get('Objects_in_box', []):
        color, shape = extract_attributes(obj_name)
        output_dict[index] = {
            "name": obj_name,
            "shape": shape,
            "color": color,
            "predicates": [],
            "init_pose": "in_box"
        }
        index += 1

    # Process Bin
    for obj_name in input_dict.get('Bin', []):
        color, shape = extract_attributes(obj_name)
        output_dict[index] = {
            "name": obj_name,
            "shape": shape,
            "color": color,
            "predicates": [],
            "init_pose": "box"
        }
        index += 1

    return output_dict


def feedback_error_decoder(error):
    error = error.decode('utf-8')
    if "SyntaxError" in error:
        pass
    elif "AssertionError" in error:
        pass
    elif "TypeError" in error:
        pass
    elif "ValueError" in error:
        pass
    else:
        pass

def initialize_csv_file(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        fieldnames = ['instance', '1', '2', '3', '4', '5', '6', '7', 'Total_num']
        writer.writerow(fieldnames)

def save2csv_v2(instance, object_dict, filename):
    objects = object_dict['Objects_out_box'] + object_dict['Objects_in_box'] + object_dict['Bin']
    objects = objects[:7]
    total_num = len(objects)
    objects += ['-'] * (7 - len(objects))

    row = [instance] + objects + [total_num]

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def save2csv(data, filename):
    fieldnames = ['instance', '1', '2', '3', '4', '5', '6', 'Total_num']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # write a csv file
        for i, (instance, objects) in enumerate(data.items(), start=1):
            out_box_items = [obj for obj, state in objects.items() if state == "out_box"]
            # in_box_items = [obj for obj, state in objects.items() if state == "in_box"]

            rows = []
            for index in range(len(out_box_items)):
                rows.append(out_box_items[index])
            for dummy in range(6-len(out_box_items)):
                rows.append(0)

            row = {
                'instance': i,
                '1': rows[0],
                '2': rows[1],
                '3': rows[2],
                '4': rows[3],
                '5': rows[4],
                '6': rows[5],
                # 'in_box': ', '.join(in_box_items),
                'Total_num': int(len(out_box_items))
            }
            writer.writerow(row)


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
