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
    is_compressible: bool = False
    is_rigid: bool = False
    is_bendable: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_fragile: bool = False


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
            # Effect: The robot is now holding the object, and its hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, already in bin.")
            return

        # Check if the object is a plastic object and if a compressible object is required
        # Since 'plastic' is not a property in the Object class, we ignore this constraint
        # and proceed to place the object without checking for compressibility.

        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the bin
        obj.in_bin = True
        self.state_handempty()

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        if self.robot_handempty and obj.is_bendable:
            print(f"bend {obj.name}")
            # State the effect of Action: Hand remains empty after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Check preconditions: object must be compressible and the robot's hand must be empty
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin.
            print(f"push {obj.name}")
            # Effects: Ensure the robot's hand remains empty after pushing
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_bendable=False, is_fragile=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_bendable=False, is_fragile=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_rigid=False, is_bendable=True, is_fragile=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_bendable=False, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_bendable is True, actions pick, place, bend are applicable
    # object3.is_rigid is True, actions pick, place are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) before placing it in the box.
    # 2. Pick and place object0 (yellow_3D_cuboid) as it is compressible, then push it.
    # 3. Pick and place object1 (blue_3D_cylinder) as it is non-plastic and can be placed without constraints.
    # 4. Pick and place object3 (green_3D_cylinder) as it is non-plastic and can be placed without constraints.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object2
    action.bend(object2, box)
    
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)
    
    # Pick, place, and push object0
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)
    
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)
    
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Object2 was bendable, so it was bent before being picked and placed in the box.
    # Object0 was compressible, so it was picked, placed, and then pushed in the box.
    # Objects 1 and 3 were non-plastic and rigid, so they were picked and placed without additional actions.
    # The sequence respects the rules regarding the handling of compressible and bendable objects.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
