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
    is_plastic: bool = False
    is_rigid: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_heavy: bool = False


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
        # Preconditions: The object must not be in the bin, and the robot hand must be empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic and any(o.is_rigid for o in box.in_bin_objects):
            # Action Description: Place an object into the box. This action can be applied to any type of object.
            # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_heavy=False)
object1 = Object(index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False)
object2 = Object(index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_plastic=True, is_rigid=False, actions pick, place are applicable
    # object1: is_rigid=True, actions pick, place are applicable
    # object2: is_rigid=True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object1 (rigid, no constraints)
    # 2. Pick and place object2 (rigid, no constraints)
    # 3. Pick and place object0 (plastic, requires a rigid object in the box)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object1, box)
    action.place(object1, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts by placing the rigid objects (object1 and object2) into the box first, as they have no constraints.
    # Once a rigid object is in the box, the plastic object (object0) can be placed according to the rules.
    # The sequence respects the constraints that plastic objects require a rigid object in the box before they can be placed.
    # No bending, folding, or pushing actions are needed as none of the objects are bendable, foldable, or compressible.

    # Finally, add this code    
    print("All task planning is done")
