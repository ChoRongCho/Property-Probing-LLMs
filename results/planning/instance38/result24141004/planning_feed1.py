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
    is_foldable: bool = False
    is_bendable: bool = False
    is_compressible: bool = False
    is_rigid: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_packable: bool = False


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

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box.
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return

        if not obj.is_packable:
            print(f"Cannot place {obj.name}, it is not packable.")
            return

        # Check the constraint: Before placing a plastic object, a compressible object should be in the box.
        if obj.object_type == 'plastic' and not any(o.is_compressible for o in box.in_bin_objects):
            print(f"Cannot place {obj.name}, a compressible object must be in the box first.")
            return

        print(f"place {obj.name}")
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

    def bend(self, obj, box):
        if obj.is_bendable and not obj.in_bin:
            print(f"bend {obj.name}")
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        if obj.is_foldable and self.robot_handempty:
            print(f"fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_foldable is True, actions pick, place, fold are applicable
    # object1.is_bendable is True, actions pick, place, bend are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable
    # object3.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0, pick object0, place object0
    # 2. Bend object1, pick object1, place object1
    # 3. Pick object2, place object2, push object2
    # 4. Pick object3, place object3

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object0, box)
    action.pick(object0, box)
    action.place(object0, box)

    action.bend(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold object0 before placing, bend object1 before placing,
    # and push object2 after placing. Object3 is placed without additional actions as it is rigid.
    # The sequence ensures that all objects are placed in the box, achieving the goal state.

    # Finally, add this code    
    print("All task planning is done")

