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
    is_compressible: bool
    is_bendable: bool

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

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The robot's hand must be empty, and the object must not already be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is holding the object
        if not self.robot_now_holding:
            print(f"Cannot place {obj.name}, the robot is not holding the object.")
            return
        
        # Check if the object is a box or obj
        if obj.object_type not in ["box", "obj"]:
            print(f"Cannot place {obj.name}, invalid object type.")
            return
        
        # Place the object in the box
        print(f"place {obj.name}")
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot state
        self.state_handempty()

    def bend(self, obj, box):
        if obj.is_bendable and self.robot_handempty:
            print(f"bend {obj.name}")
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_fragile=False)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_bendable=True, is_fragile=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_compressible is True, actions pick, place, push are applicable
    # object1: is_bendable is True, actions pick, place, bend are applicable
    # object2: is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object1 (black_1D_line) since it is bendable.
    # 2. Pick and place object0 (white_3D_cylinder) as it is compressible.
    # 3. Push object0 after placing it in the box.
    # 4. Pick and place object1 (black_1D_line) after bending.
    # 5. Pick and place object2 (red_3D_polyhedron) as it is compressible.
    # 6. Push object2 after placing it in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object1, box)  # Bend the bendable object
    action.pick(object0, box)  # Pick the compressible object
    action.place(object0, box) # Place the compressible object
    action.push(object0, box)  # Push the compressible object
    action.pick(object1, box)  # Pick the bendable object
    action.place(object1, box) # Place the bendable object
    action.pick(object2, box)  # Pick the compressible object
    action.place(object2, box) # Place the compressible object
    action.push(object2, box)  # Push the compressible object

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: 
    # - Bend the bendable object before placing it.
    # - Place a compressible object first before any plastic objects.
    # - Push compressible objects after placing them in the box.
    # - No folding is required as no objects are foldable.
    # - The sequence ensures all objects are placed in the box as per the goal state.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
