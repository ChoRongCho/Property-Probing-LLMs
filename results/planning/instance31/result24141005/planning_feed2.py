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
    is_rigid: bool
    is_bendable: bool
    is_plastic: bool

    # Additional predicates for bin_packing (max: 1)
    is_3D: bool


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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object, and the object must not be in the bin.
        if self.robot_now_holding == obj and not obj.in_bin:
            # Action Description: Place an object into the box.
            # Effects: The object is now in the bin, and the robot's hand is empty.
            print(f"place {obj.name}")
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Check if the object is bendable
        if obj.is_bendable:
            # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # Effects: Ensure the robot's hand is empty before and after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Since there is no property for compressible objects, this action cannot be executed.
        print('Cannot push')

    def fold(self, obj, box):
        # Since there is no property for foldable objects, this action cannot be executed.
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_3D=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=True, is_plastic=False, is_3D=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_3D=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, actions pick, place are applicable
    # object1: is_plastic is True, actions pick, place are applicable (requires compressible object first)
    # object2: is_bendable is True, actions pick, place, bend are applicable
    # object3: is_plastic is True, actions pick, place are applicable (requires compressible object first)
    # object4: is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it's bendable.
    # 2. Pick and place object2 (black_1D_line) as it's bendable and can be placed without constraints.
    # 3. Pick and place object0 (blue_3D_cylinder) as it's non-plastic and can be placed without constraints.
    # 4. Pick and place object4 (green_3D_cylinder) as it's non-plastic and can be placed without constraints.
    # 5. Pick and place object1 (blue_2D_rectangle) after object2 is placed (since object2 is compressible).
    # 6. Pick and place object3 (gray_1D_line) after object2 is placed (since object2 is compressible).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.pick(object0, box)
    action.place(object0, box)
    action.pick(object4, box)
    action.place(object4, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: object2 is bent before placing, and it serves as a compressible object for placing plastic objects (object1 and object3).
    # Non-plastic objects (object0 and object4) are placed without constraints.
    # The sequence ensures that all objects are placed in the box as per the goal state.

    # Finally, add this code    
    print("All task planning is done")

