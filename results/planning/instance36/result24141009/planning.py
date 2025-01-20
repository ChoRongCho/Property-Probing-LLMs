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
    is_rigid: bool = False
    is_bendable: bool = False
    is_plastic: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_2D: bool = False


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
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
            box.in_bin_objects.append(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint regarding compressible objects is applicable
        if obj.is_plastic:
            # Check if there is at least one object in the box that is not rigid (assuming non-rigid implies compressible)
            if any(not in_bin_obj.is_rigid for in_bin_obj in box.in_bin_objects):
                print(f"place {obj.name}")
                self.state_handempty()  # Update the robot state to hand empty after placing the object
                box.in_bin_objects.append(obj)  # Add the object to the box
                obj.in_bin = True  # Update the object's state to indicate it's in the bin
            else:
                print(f"Cannot place {obj.name}")
        else:
            # Non-plastic objects can be placed without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Update the robot state to hand empty after placing the object
            box.in_bin_objects.append(obj)  # Add the object to the box
            obj.in_bin = True  # Update the object's state to indicate it's in the bin

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        if self.robot_handempty and obj.is_bendable and not obj.is_plastic:
            print(f"bend {obj.name}")
            # Assuming the effect is that the object is now bent and ready to be placed in the box
            self.state_handempty()  # Ensure the hand is empty after bending
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            # Preconditions: The robot's hand must be empty to fold the object
            if self.robot_handempty:
                print(f"fold {obj.name}")
                # Effects: The robot's hand remains empty after folding
                self.state_handempty()
            else:
                print(f"Cannot fold {obj.name} because the robot is holding something.")
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True, is_2D=True)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_foldable is True, actions pick, place, fold are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_bendable is True, actions pick, place, bend are applicable
    # object3.is_plastic is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 (foldable) -> pick object0 -> place object0
    # 2. Bend object2 (bendable) -> pick object2 -> place object2
    # 3. Pick object1 (rigid) -> place object1
    # 4. Pick object3 (plastic) -> place object3 (after object0 or object2 is in the box)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object0
    action.fold(object0, box)
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)
    
    # Bend object2
    action.bend(object2, box)
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)
    
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)
    
    # Pick and place object3 (plastic, after a compressible object is in the box)
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold object0 before placing, bend object2 before placing,
    # and ensure a compressible object (object0 or object2) is in the box before placing object3 (plastic).
    # Object1 is rigid and can be placed without constraints. The sequence ensures all objects are packed.

    # Finally, add this code    
    print("All task planning is done")
