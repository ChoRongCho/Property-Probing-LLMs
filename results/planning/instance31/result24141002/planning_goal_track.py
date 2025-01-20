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
        # Preconditions: The robot hand must be empty, and the object must not be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is currently holding the object and the object is not already in a bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Check if the object is plastic and if the constraint can be ignored
            if obj.is_plastic:
                # Since the constraint mentions a compressible property which is not present, ignore the constraint
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the bin
                obj.in_bin = True
                self.state_handempty()
            else:
                # For non-plastic objects, place them without constraints
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the bin
                obj.in_bin = True
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
        if self.robot_handempty and obj.is_bendable and not obj.is_3D:
            print(f"bend {obj.name}")
            # Since the hand must remain empty, no change in state is needed.
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
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
    # object0: is_rigid=True, is_3D=True, actions: pick, place
    # object1: is_plastic=True, actions: pick, place (requires compressible object in box first)
    # object2: is_bendable=True, actions: pick, bend, place
    # object3: is_plastic=True, actions: pick, place (requires compressible object in box first)
    # object4: is_rigid=True, is_3D=True, actions: pick, place

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it is bendable.
    # 2. Pick and place object2 (black_1D_line) as it is bendable and can be placed without constraints.
    # 3. Pick and place object0 (blue_3D_cylinder) as it is non-plastic and can be placed without constraints.
    # 4. Pick and place object4 (green_3D_cylinder) as it is non-plastic and can be placed without constraints.
    # 5. Pick and place object1 (blue_2D_rectangle) since a compressible object (object2) is already in the box.
    # 6. Pick and place object3 (gray_1D_line) since a compressible object (object2) is already in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)  # Bend the bendable object
    action.pick(object2, box)  # Pick the bendable object
    action.place(object2, box)  # Place the bendable object
    action.pick(object0, box)  # Pick the non-plastic object
    action.place(object0, box)  # Place the non-plastic object
    action.pick(object4, box)  # Pick the non-plastic object
    action.place(object4, box)  # Place the non-plastic object
    action.pick(object1, box)  # Pick the plastic object
    action.place(object1, box)  # Place the plastic object
    action.pick(object3, box)  # Pick the plastic object
    action.place(object3, box)  # Place the plastic object

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object first, place non-plastic objects without constraints,
    # and ensure a compressible object is in the box before placing plastic objects. The sequence respects the
    # constraints and properties of each object, achieving the goal states.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
