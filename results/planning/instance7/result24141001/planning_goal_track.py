from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # physical state of an object for bin_packing
    in_bin: bool

    # Object physical properties 
    is_plastic: bool
    is_compressible: bool

    # Additional predicates for bin_packing (max: 1)
    is_fragile: bool


@dataclass
class Box:
    # Basic dataclass
    index: int
    name: str

    # Predicates for box
    object_type: str  # box or obj
    in_bin_objects: list                


class Action:
    def __init__(self, name: str = "UR5"):
        self.name = name    
        self.robot_handempty = True
        self.robot_now_holding = False

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The robot's hand must be empty and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. 
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the object is considered in the box.
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is plastic and ensure a compressible object is already in the box
        if obj.is_plastic:
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # If the robot is holding the object and the object is not already in a bin
        if self.robot_now_holding == obj and not obj.in_bin:
            print(f"place {obj.name}")
            # Effect: Update the state to reflect the object is now in the bin
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Preconditions: The object must be compressible and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin. 
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after pushing.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_compressible=False, is_fragile=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=False, is_compressible=True, is_fragile=False)
object2 = Object(index=2, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True, is_compressible=False, is_fragile=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_compressible=True, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_plastic is True, actions pick, place are applicable with constraints
    # the object1.is_compressible is True, actions pick, place, push are applicable
    # the object2.is_plastic is True, actions pick, place are applicable with constraints
    # the object3.is_compre/home/changmin/anaconda3/envs/pddlv2/bin/python /home/changmin/PycharmProjects/OPTPlan/main.py --task_name bin_packing --exp_name 1 --exp_number 1 --is_save 1 --api_json setting.json --robot_json robot.json --max_feedback 5
    #
    # ---Start validating---
    #
    # /home/changmin/anaconda3/envs/pddlv2/lib/python3.11/site-packages/torch/functional.py:507: UserWarning: torch.meshgrid: in an upcoming release, it will be required to pass the indexing argument. (Triggered internally at /opt/conda/conda-bld/pytorch_1708025845868/work/aten/src/ATen/native/TensorShape.cpp:3549.)
    #   return _VF.meshgrid(tensors, **kwargs)  # type: ignore[attr-defined]
    # final text_encoder_type: bert-base-uncased
    # /home/changmin/anaconda3/envs/pddlv2/lib/python3.11/site-packages/transformers/tokenization_utils_base.py:1601: FutureWarning: `clean_up_tokenization_spaces` was not set. It will be set to `True` by default. This behavior will be depracted in transformers v4.45, and will be then set to `False` by default. For more details check this issue: https://github.com/huggingface/transformers/issues/31884
    #   warnings.warn(
    # planning/instance1/result24141001/planning.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141002/planning.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141003/planning_feed1.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141004/planning.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141005/planning.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141006/planning_feed1.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141007/planning.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141008/planning_feed2.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141009/planning_feed5.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # Cannot place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance1/result24141010/planning.py
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance2/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141002/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141003/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141004/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141005/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141006/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141007/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141008/planning.py
    # bend black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141009/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance2/result24141010/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance3/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141002/planning.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141003/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141004/planning.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141005/planning.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141006/planning.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141007/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141008/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141009/planning.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance3/result24141010/planning.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance4/result24141001/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141002/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141003/planning_feed5.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick yellow_2D_rectangle
    # fold yellow_2D_rectangle
    # Cannot place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141004/planning.py
    # pick yellow_2D_rectangle
    # fold yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141005/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141006/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141007/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141008/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141009/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance4/result24141010/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance5/result24141001/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141002/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141003/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141005/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141006/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141007/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141008/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141009/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance5/result24141010/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance6/result24141001/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141002/planning.py
    # pick yellow_2D_rectangle
    # fold yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141003/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141005/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141006/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141007/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141008/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141009/planning_feed5.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # Cannot pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance6/result24141010/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance7/result24141001/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141002/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141003/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141005/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141006/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141007/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141008/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141009/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance7/result24141010/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance8/result24141001/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141002/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141003/planning.py
    # fold yellow_2D_rectangle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141004/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141005/planning_feed3.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141006/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141007/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141008/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141009/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance8/result24141010/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance9/result24141001/planning_feed1.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141002/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141003/planning_feed4.py
    # pick transparent_2D_circle
    # fold transparent_2D_circle
    # place transparent_2D_circle
    # pick black_1D_line
    # bend black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141004/planning_feed2.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # push transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141005/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141006/planning_feed2.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # push transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141007/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141008/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141009/planning_feed2.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # push transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance9/result24141010/planning_feed2.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance10/result24141001/planning_feed2.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # Cannot pick beige_1D_line
    # Cannot place beige_1D_line because it is not being held
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141002/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141003/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141004/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141005/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141006/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141007/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141008/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141009/planning_feed1.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance10/result24141010/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance11/result24141001/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141002/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141003/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141004/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141005/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141006/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141007/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141008/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141009/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance11/result24141010/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance12/result24141001/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141002/planning.py
    # fold transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141003/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141004/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141005/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141006/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141007/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141008/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141009/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance12/result24141010/planning.py
    # fold transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance13/result24141001/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # fold yellow_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141002/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141003/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141004/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141005/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141006/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # fold yellow_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141007/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141008/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141009/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance13/result24141010/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick red_3D_cuboid
    # place red_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance14/result24141001/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141002/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141003/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141005/planning_feed4.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141006/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141007/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141008/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141009/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance14/result24141010/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance15/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141002/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141003/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141004/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141005/planning_feed1.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141006/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141007/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141008/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141009/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance15/result24141010/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance16/result24141001/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141002/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141003/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141005/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141006/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141007/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141008/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141009/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance16/result24141010/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance17/result24141001/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141002/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141003/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141004/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141005/planning_feed1.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141006/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141007/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141008/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141009/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance17/result24141010/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance18/result24141001/planning_feed4.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141002/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141003/planning_feed3.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # push white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # push blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141004/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141005/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141006/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141007/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141008/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141009/planning_feed5.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # Cannot pick gray_1D_line
    # Cannot place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance18/result24141010/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance19/result24141001/planning.py
    # fold transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141002/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141003/planning_feed2.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141004/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141005/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141006/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141007/planning.py
    # fold transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141008/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141009/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance19/result24141010/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance20/result24141001/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141002/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141003/planning_feed1.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141004/planning_feed5.py
    # pick white_3D_cylinder
    # Cannot place white_3D_cylinder: No compressible object in the box.
    # Cannot push white_3D_cylinder
    # Cannot pick brown_3D_cylinder
    # Cannot place brown_3D_cylinder: Preconditions not met.
    # Cannot push brown_3D_cylinder
    # Cannot pick white_3D_cuboid
    # Cannot place white_3D_cuboid: Preconditions not met.
    # Cannot pick beige_1D_line
    # Cannot place beige_1D_line: Preconditions not met.
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141005/planning_feed1.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141006/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141007/planning.py
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141008/planning_feed1.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141009/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance20/result24141010/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance21/result24141001/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141002/planning_feed2.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick yellow_2D_rectangle
    # fold yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick transparent_2D_circle
    # fold transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141003/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141004/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141005/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141006/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141007/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141008/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141009/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance21/result24141010/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance22/result24141001/planning.py
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141002/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141003/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141004/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141005/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141006/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141007/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141008/planning_feed1.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141009/planning_feed1.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance22/result24141010/planning.py
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick white_3D_cuboid
    # place white_3D_cuboid
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance23/result24141001/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141002/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141003/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141005/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141006/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141007/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141008/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141009/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance23/result24141010/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance24/result24141001/planning.py
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141002/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141003/planning.py
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141004/planning.py
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141005/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141006/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141007/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141008/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141009/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance24/result24141010/planning.py
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance25/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141002/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141003/planning_feed1.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141004/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141005/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141006/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141007/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141008/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141009/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance25/result24141010/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance26/result24141001/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141002/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141003/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141005/planning.py
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141006/planning_feed1.py
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141007/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141008/planning.py
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141009/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance26/result24141010/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # fold transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance27/result24141001/planning.py
    #
    # Traceback (most recent call last):
    #   File "/home/changmin/PycharmProjects/OPTPlan/planning/instance27/result24141001/planning.py", line 135, in <module>
    #     box = Box(index=0, name='box', in_bin_objects=[])
    #           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # TypeError: Box.__init__() missing 1 required positional argument: 'object_type'
    #
    #
    #
    #
    # planning/instance27/result24141002/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141003/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141004/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141005/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141006/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick beige_1D_line
    # place beige_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141007/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141008/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141009/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance27/result24141010/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance28/result24141001/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141002/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141003/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141004/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141005/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141006/planning_feed2.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141007/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141008/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141009/planning.py
    # bend black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance28/result24141010/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance29/result24141001/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141002/planning.py
    # fold yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141003/planning_feed1.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141004/planning_feed2.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141005/planning.py
    # fold yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141006/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141007/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141008/planning.py
    # fold yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141009/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance29/result24141010/planning.py
    # pick yellow_3D_cuboid
    # place yellow_3D_cuboid
    # push yellow_3D_cuboid
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance30/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141002/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141003/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141004/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141005/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141006/planning_feed1.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141007/planning.py
    # bend black_1D_line
    # fold transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141008/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141009/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance30/result24141010/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance31/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141002/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141003/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141004/planning_feed1.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141005/planning_feed2.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141006/planning_feed2.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141007/planning_feed2.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141008/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141009/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance31/result24141010/planning_feed3.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_3D_cylinder
    # place blue_3D_cylinder
    # push blue_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # push green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance32/result24141001/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141002/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141003/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141004/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141005/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141006/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141007/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141008/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141009/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance32/result24141010/planning_feed1.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance33/result24141001/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141002/planning_feed1.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141003/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141004/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141005/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141006/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141007/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141008/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141009/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance33/result24141010/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance34/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141002/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141003/planning.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141004/planning_feed2.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141005/planning_feed1.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141006/planning_feed2.py
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141007/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141008/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141009/planning.py
    # bend black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance34/result24141010/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick white_3D_cylinder
    # place white_3D_cylinder
    # push white_3D_cylinder
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance35/result24141001/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141002/planning.py
    # fold transparent_2D_circle
    # bend black_1D_line
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick black_1D_line
    # place black_1D_line
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141003/planning_feed1.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141004/planning_feed1.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141005/planning.py
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141006/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141007/planning.py
    # bend black_1D_line
    # fold transparent_2D_circle
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141008/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141009/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance35/result24141010/planning.py
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick blue_2D_rectangle
    # place blue_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance36/result24141001/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141002/planning_feed2.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push yellow_2D_rectangle
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141003/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # push yellow_2D_rectangle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141004/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141005/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # push yellow_2D_rectangle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141006/planning_feed2.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141007/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # push yellow_2D_rectangle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141008/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # push yellow_2D_rectangle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141009/planning.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance36/result24141010/planning_feed1.py
    # fold yellow_2D_rectangle
    # pick yellow_2D_rectangle
    # place yellow_2D_rectangle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # push black_1D_line
    # pick beige_1D_line
    # place beige_1D_line
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance37/result24141001/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141002/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141003/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141004/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141005/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141006/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141007/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141008/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141009/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick brown_3D_cylinder
    # place brown_3D_cylinder
    # push brown_3D_cylinder
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance37/result24141010/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick beige_1D_line
    # place beige_1D_line
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick gray_1D_line
    # place gray_1D_line
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # planning/instance38/result24141001/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141002/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141003/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141004/planning_feed2.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141005/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141006/planning.py
    # fold transparent_2D_circle
    # bend black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # pick black_1D_line
    # place black_1D_line
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141007/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141008/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141009/planning_feed1.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # planning/instance38/result24141010/planning.py
    # fold transparent_2D_circle
    # pick transparent_2D_circle
    # place transparent_2D_circle
    # bend black_1D_line
    # pick black_1D_line
    # place black_1D_line
    # pick red_3D_polyhedron
    # place red_3D_polyhedron
    # push red_3D_polyhedron
    # pick green_3D_cylinder
    # place green_3D_cylinder
    # All task planning is done
    #
    #
    #
    #
    #
    # --------------------------------------------------
    # Positive Rate: 98.1579%
    # Negative Rate: 1.5789%
    # Error Rate: 0.2632%
    # --------------------------------------------------
    # Negative:  exp24141009, instance:1
    # Negative:  exp24141003, instance:4
    # Negative:  exp24141009, instance:6
    # Negative:  exp24141001, instance:10
    # Negative:  exp24141009, instance:18
    # Negative:  exp24141004, instance:20
    # --------------------------------------------------
    # Error:  exp24141001, instance:27
    # --------------------------------------------------
    # Done
    #
    # Process finished with exit code 0ssible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object1 (compressible) into the box, then push it.
    # 2. Pick and place object3 (compressible) into the box, then push it.
    # 3. Pick and place object0 (plastic) into the box (after a compressible object is in the box).
    # 4. Pick and place object2 (plastic) into the box (after a compressible object is in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts with placing compressible objects (object1 and object3) into the box and pushing them,
    # as they have no constraints and allow for subsequent placement of plastic objects.
    # Once a compressible object is in the box, plastic objects (object0 and object2) can be placed without issues.
    # This sequence respects all rules and achieves the goal state for all objects.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
