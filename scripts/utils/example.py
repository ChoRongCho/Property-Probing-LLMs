import json
import os.path
import random

OCPS = """
from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # physical state of an object
    pushed: bool
    folded: bool
    in_bin: bool

    # Object physical properties
    is_compressible: bool
    is_bendable: bool
    is_plastic: bool
    is_rigid: bool

    # pre-conditions and effects for bin_packing task planning (max: 2)
    is_heavy: bool
    is_fragile: bool

@dataclass
class Box:
    # Basic dataclass
    index: int
    name: str

    # Predicates for box
    object_type: str  # box or obj
    in_bin_objects: list                
"""

RCPS = """
class Robot:
    def __init__(self,
                 name: str = "OpenManipulator",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = False
    
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Pre-conditions: Object is not in the bin and robot hand is empty
        if not obj.in_bin and self.robot_handempty:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Pre-conditions: Robot is holding the object
        if self.robot_now_holding == obj:
            # Check if a compressible object is already in the bin if the object is plastic
            if obj.is_plastic and not any(o.is_compressible for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} because no compressible object is in the bin")
            else:
                obj.in_bin = True
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin):
        # Pre-conditions: Object is compressible, not bendable, and robot hand is empty
        if obj.is_compressible and not obj.is_bendable and self.robot_handempty:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Pre-conditions: Object is foldable, not bendable, and robot hand is empty
        if obj.is_bendable and not obj.is_bendable and self.robot_handempty:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Pre-conditions: Object is in the bin
        if obj in bin.in_bin_objects:
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass
"""


OBJS = [
    "red_3D_cuboid",
    "white_3D_cuboid",
    "yellow_3D_cuboid",
    "blue_3D_cylinder",
    "white_3D_cylinder",
    "blue_2D_rectangle",
    "yellow_2D_rectangle",
    "transparent_2D_circle",
    "beige_1D_line",
    "black_1D_line",
    "gray_1D_line",
    "red_3D_polyhedron",
    "brown_3D_cylinder",
    "green_3D_cylinder"
]

DICT_LIST = [
    {'Objects_out_box': [OBJS[0],OBJS[1],OBJS[13]], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[1],OBJS[9],OBJS[11],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[4],OBJS[5],OBJS[9],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[2],OBJS[3],OBJS[6],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[2],OBJS[3],OBJS[8],OBJS[11],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[2],OBJS[4],OBJS[6],OBJS[10],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[2],OBJS[5],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[3],OBJS[4],OBJS[5],OBJS[6],OBJS[10],OBJS[12],], 'Objects_in_box': [], 'Bin': []},

    {'Objects_out_box': [OBJS[0],OBJS[3],OBJS[7],OBJS[9],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[3],OBJS[8],OBJS[12],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[3],OBJS[11],OBJS[12]], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[4],OBJS[7],OBJS[8],OBJS[11],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[0],OBJS[5],OBJS[6],OBJS[12],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[2],OBJS[3],OBJS[5],OBJS[8],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[2],OBJS[4],OBJS[5],OBJS[9],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[2],OBJS[4],OBJS[6],OBJS[12]], 'Objects_in_box': [], 'Bin': []},

    {'Objects_out_box': [OBJS[1],OBJS[3],OBJS[4],OBJS[8],OBJS[10],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[3],OBJS[5],OBJS[10],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[4],OBJS[7],OBJS[10],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[4],OBJS[8],OBJS[11],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[5],OBJS[6],OBJS[7],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[1],OBJS[10],OBJS[11],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[2],OBJS[3],OBJS[4],OBJS[6],OBJS[11],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[2],OBJS[3],OBJS[5],OBJS[7],OBJS[11],OBJS[13],], 'Objects_in_box': [], 'Bin': []},

    {'Objects_out_box': [OBJS[2],OBJS[3],OBJS[9],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[2],OBJS[4],OBJS[7],OBJS[10],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[2],OBJS[4],OBJS[8],OBJS[12],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[2],OBJS[5],OBJS[9],OBJS[11],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[2],OBJS[6],OBJS[7],OBJS[11],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[3],OBJS[4],OBJS[7],OBJS[9],OBJS[11],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[3],OBJS[5],OBJS[9],OBJS[10],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[4],OBJS[5],OBJS[6],OBJS[7],OBJS[11],OBJS[12],], 'Objects_in_box': [], 'Bin': []},

    {'Objects_out_box': [OBJS[4],OBJS[8],OBJS[10],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[4],OBJS[9],OBJS[11],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[5],OBJS[7],OBJS[8],OBJS[9],OBJS[12],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[6],OBJS[8],OBJS[9],OBJS[10],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[7],OBJS[8],OBJS[9],OBJS[10],OBJS[11],OBJS[12],], 'Objects_in_box': [], 'Bin': []},
    {'Objects_out_box': [OBJS[7],OBJS[9],OBJS[11],OBJS[13],], 'Objects_in_box': [], 'Bin': []},
]

GOALS = [
    "Pack all the objects except for the white ones.",
    "Pack all the objects.",
    "Pack all the objects except for plastic ones.",
    "Pack all the objects.",
    "Pack all the objects.",

    "Pack all the objects except for the red ones.",
    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects except for rigid ones.",
    "Pack all the objects except for green ones.",

    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects except for the 2D ones.",
    "Pack all the objects.",
    "Pack all the objects.",

    "Pack all the objects.",
    "Pack all the objects except for rigid ones.",
    "Pack all the objects except for the 2D ones.",
    "Pack all the objects.",
    "Pack all the objects except for red ones.",

    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects except for the blue ones.",
    "Pack all the objects except for the plastic ones.",
    "Pack all the objects.",

    "Pack all the objects except for the foldable ones.",
    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects except for the 1D ones.",
    "Pack all the objects.",

    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects.",

    "Pack all the objects.",
    "Pack all the objects, except for the brown one.",
    "Pack all the objects.",
]

PROPERTIES = [
    "is_plastic",
    "is_rigid",
    "is_compressible",
    "is_rigid",
    "is_compressible",
    "is_plastic",
    "is_foldable",
    "is_foldable",
    "is_rigid",
    "is_bendable",
    "is_plastic",
    "is_compressible",
    "is_compressible",
    "is_rigid",
]


def get_pseudo_json():
    data_dir = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/pseudo_database.json"
    with open(data_dir, 'r') as file:
        data = json.load(file)
        bin_packing_data = data["bin_packing"]
    return bin_packing_data


def get_random_names(data, min_count=3, max_count=5):
    index_map = {}
    for name, details in data.items():
        index = details['index']
        if index not in index_map:
            index_map[index] = []
        index_map[index].append(name)

    selected_indices = random.sample(range(1, 17), random.randint(min_count, max_count))

    selected_names = []
    for idx in selected_indices:
        if idx in index_map:
            # 해당 인덱스의 이름 중 랜덤하게 하나 선택
            selected_names.append(random.choice(index_map[idx]))

    return selected_names


def get_random_goal():
    goal_list = [
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects except for foldable ones.",
        "Pack all the objects except for rigid ones.",
        "Pack all the objects except for the white ones.",
        "Pack all the objects except for the yellow ones.",
        "Pack all the objects except for the 2D ones.",
    ]
    random_goal = random.choice(goal_list)
    print(random_goal)


def make_instruction():
    for i in range(1, 39):
        print(i)
        file_name = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3/instance{i}/task_instruction.json"

        data = {
            "bin_packing": {
                "for_user": {
                    "constraints": "packing problem",
                    "rule_and_goal": {
                        "rule": "give conditions to the actions",
                        "goal": "the objective of the task"
                    }
                },
                "rules": {
                    "1": "Before place a plastic object, compressible object should be in the box before. However, if there is no compressible object, place it.",
                    "2": "Don't push or fold plastic object.",
                    "3": "If there is any foldable object, fold it before place it in the box",
                    "4": "Only push compressible objects after placing items in the bin."
                },
                "goals": GOALS[i-1]
            }
        }

        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)



def pseudo_gt():
    gt = [
        [],
        [],
        [],
        [],
    ]
    return gt










def main():
    packing_data = get_pseudo_json()
    selected_names = get_random_names(packing_data)
    dict_index = {'Objects_out_box': selected_names, 'Objects_in_box': [], 'Bin': []}
    print(dict_index)


if __name__ == '__main__':
    for i in range(38):
        print(f"Instance{i+1}:", DICT_LIST[i]['Objects_out_box'])