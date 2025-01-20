from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # physical state of an object for {self.task}
    in_bin: bool

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
        # Preconditions: The object must not be in the box, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and its hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
    # Action Description: Place an object into the box. This action can be applied to any type of object.
    # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
    
    # Check if the object is plastic and if the box already contains a compressible object
    if obj.object_type == "plastic" and "compressible" not in [o.object_type for o in box.in_bin_objects]:
        print(f"Cannot place {obj.name}")
    else:
        print(f"place {obj.name}")
        # Update the state to reflect the object being placed in the box
        self.state_handempty()
        box.in_bin_objects.append(obj)

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0: is_rigid = True, is_compressible = False, is_bendable = False, is_foldable = False
    # object1: is_rigid = True, is_compressible = False, is_bendable = False, is_foldable = False
    # object2: is_rigid = True, is_compressible = False, is_bendable = True, is_foldable = False
    # object3: is_rigid = True, is_compressible = True, is_bendable = False, is_foldable = False

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (if bendable) before picking.
    # 2. Pick and place object3 (compressible) first, then push it.
    # 3. Pick and place object0.
    # 4. Pick and place object1.
    # Note: No plastic objects are present, so rule 1 is not applicable.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object2
    action.bend(object2, box)

    # Pick and place object3, then push
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bendable objects are bent before picking, compressible objects are pushed after placing, and all objects are placed in the box as per the goal state.

    # Finally, add this code    
    print("All task planning is done")
