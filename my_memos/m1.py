import csv
import os.path


def save_to_csv(data):
    fieldnames = ['instance', 'out_box', 'in_box', 'Total_num']
    filename = os.path.join("/home/changmin/PycharmProjects/OPTPlan/result", "output.csv")
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # write a csv file
        for i, (instance, objects) in enumerate(data.items(), start=1):
            out_box_items = [obj for obj, state in objects.items() if state == "out_box"]
            in_box_items = [obj for obj, state in objects.items() if state == "in_box"]

            row = {
                'instance': i,  # 인스턴스 번호
                'out_box': ', '.join(out_box_items),
                'in_box': ', '.join(in_box_items),
                'Total_num': int(len(out_box_items) + len(in_box_items))   # 총 객체 수
            }
            writer.writerow(row)


def main():
    instance = {
        0: {'name': 'yellow_3D_cuboid', 'shape': '3D_cuboid', 'color': 'yellow',
            'predicates': ['is_soft', 'is_elastic'],
            'init_pose': 'out_box'},
        1: {'name': 'black_2D_circle', 'shape': '2D_circle', 'color': 'black', 'predicates': ['is_rigid', 'is_fragile'],
            'init_pose': 'out_box'},
        2: {'name': 'blue_2D_loop', 'shape': '2D_loop', 'color': 'blue', 'predicates': [], 'init_pose': 'out_box'},
        3: {'name': 'white_box', 'shape': 'box', 'color': 'white', 'predicates': [], 'init_pose': 'box'}}

    test_num1 = {'instance1': {}}

    for i, data in instance.items():
        test_num1['instance1'][data['name']] = data['init_pose']
    print(test_num1)
    save_to_csv(test_num1)


if __name__ == '__main__':
    instances = {'instance1': {'brown_3D_cuboid': 'out_box',
                               'black_2D_circle': 'out_box',
                               'blue_2D_loop': 'out_box',
                               'white_box': 'box'},
                 'instance2': {'white_2D_loop': 'out_box', 'black_3D_cylinder': 'out_box', 'black_2D_loop': 'in_box',
                               'white_box': 'box'},
                 'instance3': {'red_3D_polyhedron': 'out_box', 'yellow_3D_cylinder': 'out_box',
                               'white_2D_loop': 'out_box',
                               'white_box': 'box'},
                 'instance4': {'white_2D_loop': 'out_box', 'black_2D_loop': 'out_box', 'yellow_3D_cuboid': 'in_box',
                               'white_box': 'box'}}
    save_to_csv(instances)
