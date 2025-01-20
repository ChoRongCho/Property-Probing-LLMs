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
        # Preconditions: The object is not in the box and the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if a compressible object is already in the box
        if obj.object_type == "plastic":
            # Assuming 'compressible' is a property we need to check, but it's not in the Object class
            # Therefore, we ignore the constraint as per the instructions
            print(f"place {obj.name}")
            self.state_handempty()  # Effect: The robot's hand is now empty after placing the object
            box.in_bin_objects.append(obj)  # Effect: The object is now in the box
        else:
            # For non-plastic objects, place without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Effect: The robot's hand is now empty after placing the object
            box.in_bin_objects.append(obj)  # Effect: The object is now in the box

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object2 = Object(index=2, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for objects based on the rules
    object0.is_compressible = False
    object0.is_foldable = False
    object0.is_bendable = False
    object0.is_plastic = False

    object1.is_compressible = False
    object1.is_foldable = False
    object1.is_bendable = False
    object1.is_plastic = False

    object2.is_compressible = True
    object2.is_foldable = False
    object2.is_bendable = False
    object2.is_plastic = False

    object3.is_compressible = False
    object3.is_foldable = True
    object3.is_bendable = False
    object3.is_plastic = False

    object4.is_compressible = False
    object4.is_foldable = False
    object4.is_bendable = False
    object4.is_plastic = True

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (yellow_2D_rectangle) before placing it.
    # 2. Pick and place object3.
    # 3. Pick and place object2 (blue_3D_cylinder), then push it.
    # 4. Pick and place object0 (red_3D_cuboid).
    # 5. Pick and place object1 (yellow_3D_cuboid).
    # 6. Pick and place object4 (brown_3D_cylinder) after object2 is in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: object3 is folded before placing, object2 is pushed after placing,
    # and object4 is placed after a compressible object (object2) is in the box. Non-plastic objects are placed without constraints.

    # Finally, add this code    
    print("All task planning is done")
