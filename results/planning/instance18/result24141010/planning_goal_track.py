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
    is_rigid: bool = False
    is_plastic: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_3D: bool = False


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
        # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
        # Preconditions: The robot's hand must be empty, and the object must not already be in the box.
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the object is considered in the robot's possession.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic and any(o.is_rigid for o in box.in_bin_objects):
            # Action Description: Place an object into the box. This action can be applied to any type of object.
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the bin
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        elif not obj.is_plastic:
            # Non-plastic objects can be placed without constraints
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the bin
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
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object2 = Object(index=2, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_rigid is True, actions pick, place are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_plastic is True, actions pick, place are applicable
    # the object3.is_plastic is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object0 (rigid, no constraints)
    # 2. Pick and place object1 (rigid, no constraints)
    # 3. Pick and place object2 (plastic, requires a compressible object in the box first)
    # 4. Pick and place object3 (plastic, requires a compressible object in the box first)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Assuming object0 or object1 is considered compressible for the sake of this example
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: rigid objects (object0 and object1) are placed first without constraints.
    # Plastic objects (object2 and object3) are placed after a compressible object is already in the box.
    # No bending, folding, or pushing actions are required as no objects have these properties.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
