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
        self.robot_now_holding = None

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None

    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object, and the object must not already be in the bin.
        if self.robot_now_holding == obj and not obj.in_bin:
            # Check if the object is plastic and if the constraint applies
            if obj.is_plastic:
                # Ensure there's at least one compressible object already in the box
                if not any(o.is_compressible for o in box.in_bin_objects):
                    print(f"Cannot place {obj.name}, no compressible object in the box.")
                    return

            # Action Description: Place an object into the box.
            print(f"place {obj.name}")
            
            # Update the state to reflect the object is now in the bin
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            
            # Update the robot's state to hand empty after placing the object
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # State the effect of Action: Hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and not plastic, and it must be in the bin.
        if obj.is_compressible and not obj.is_plastic and obj.in_bin:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effects: Ensure the robot's hand is empty after the action.
            self.state_handempty()
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
    # object3: is_bendable is True, actions pick, place, bend are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (black_1D_line) since it is bendable.
    # 2. Pick and place object3 (black_1D_line) into the box.
    # 3. Pick and place object1 (white_3D_cylinder) into the box, then push it since it is compressible.
    # 4. Pick and place object0 (red_3D_cuboid) into the box, ensuring object1 is already in the box.
    # 5. Pick and place object2 (blue_2D_rectangle) into the box, ensuring object1 is already in the box.

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
    action.place(object0, box)  # Place the plastic object after a compressible one

    action.pick(object2, box)
    action.place(object2, box)  # Place the plastic object after a compressible one

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing, place a compressible object before plastic ones, and push compressible objects after placing. The actions ensure all objects reach their goal state of being in the bin.

    # Finally, add this code    
    print("All task planning is done")

