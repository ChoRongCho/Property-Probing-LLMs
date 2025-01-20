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
    is_bendable: bool
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
        # Action Description: Pick an object that is not in the box. 
        # The action does not include the 'place' action and can be applied to any type of object.
        
        # Preconditions: The object must not already be in the box, and the robot hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return

        # Check if the robot is holding the object
        if not self.robot_now_holding:
            print(f"Cannot place {obj.name}, the robot is not holding the object.")
            return

        # Check the constraint for placing a plastic object
        if obj.is_plastic:
            # Check if there's a compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}, a compressible object must be in the box first.")
                return

        # Place the object in the box
        print(f"place {obj.name}")
        box.in_bin_objects.append(obj)
        obj.in_bin = True

        # Update the robot's state
        self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if hasattr(obj, 'is_bendable') and obj.is_bendable and hasattr(obj, 'is_plastic') and not obj.is_plastic:
            # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # Ensure the robot's hand is empty before and after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            print(f"push {obj.name}")
            # Ensure the robot's hand is empty before and after the action
            self.state_handempty()
            # Additional effects can be added here if necessary
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_bendable=False, is_compressible=False, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_bendable=False, is_compressible=True, is_fragile=False)
object2 = Object(index=2, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True, is_bendable=False, is_compressible=False, is_fragile=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_plastic=False, is_bendable=True, is_compressible=False, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_plastic is True, is_compressible is False, actions pick, place are applicable
    # object1: is_compressible is True, actions pick, place, push are applicable
    # object2: is_plastic is True, is_compressible is False, actions pick, place are applicable
    # object3: is_bendable is True, actions bend, pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (black_1D_line) before picking and placing it.
    # 2. Pick and place object1 (white_3D_cylinder) first, then push it.
    # 3. Pick and place object0 (red_3D_cuboid) after object1 is in the box.
    # 4. Pick and place object2 (blue_2D_rectangle) after object1 is in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)  # Bend the bendable object
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)  # Push the compressible object

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing it, place a compressible object first
    # to allow plastic objects to be placed, and push the compressible object after placing it. The sequence ensures
    # that all objects are placed in the box according to their physical properties and the given constraints.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
