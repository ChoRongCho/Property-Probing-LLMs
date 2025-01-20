import json
import os


def get_json_data(json_path):
    with open(json_path, "r") as file:
        data = json.load(file)
    return data


def convert_object_format(objects_list):
    bin_packing = {}

    for objects in objects_list:
        for obj in objects.values():
            name = obj["name"]
            if name in bin_packing:
                continue

            color = obj["color"]
            shape_split = obj["shape"].split('_')
            dimension = shape_split[0]
            shape = '_'.join(shape_split[1:])

            bin_packing[name] = {
                "color": color,
                "dimension": dimension,
                "shape": shape,
                "properties": []
            }

    return {"bin_packing": bin_packing}


def main():
    data_dir = "/home/changmin/PycharmProjects/OPTPlan/data"
    all_data = []
    for i in range(1, 36):
        json_path = os.path.join(data_dir, "bin_packing", "planning", f"instance{i}", "planning_object_gt.json")
        data = get_json_data(json_path)
        all_data.append(data)

    converted_data = convert_object_format(all_data)
    print(json.dumps(converted_data, indent=4))
    with open("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_object_gt.json", "w") as file:
        json.dump(converted_data, file, indent=4)
        file.close()


if __name__ == '__main__':
    main()
