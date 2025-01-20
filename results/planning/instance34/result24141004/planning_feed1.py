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

# only write a code here without example instantiation
# Note! If a predicate required by the constraints is not defined in the class Object, ignore the constraints!!!
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
        # Preconditions: The object is not in the box and the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the robot is holding the object
        if self.robot_now_holding == obj:
            # Check if the object is a plastic object and if a compressible object is already in the box
            if obj.object_type == "plastic":
                compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
                if not compressible_in_box:
                    print(f"Cannot place {obj.name}")
                    return
            
            # Place the object in the box
            print(f"place {obj.name}")
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()  # Update the robot's state to hand empty after placing the object
            
        else:
            print(f"Cannot place {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check if the object is compressible and the robot's hand is empty
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
            # No change in the robot's state as the hand remains empty
            # Effects: The object is considered pushed in the box
            # (No explicit state change needed in this simplified context)
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

# Assuming there is a box, but no specific details provided in the input
box = Box(index=0, name='default_box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0 is compressible, actions pick, place, push are applicable
    # object1 is bendable, actions pick, place, bend are applicable
    # object2 is compressible, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick object0, place it in the box, then push it.
    # 2. Bend object1, pick it, and place it in the box.
    # 3. Pick object2, place it in the box, then push it.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='default_box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Step 1: Handle object0
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    # Step 2: Handle object1
    action.bend(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    # Step 3: Handle object2
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Object0 and object2 are compressible, so they are picked, placed, and then pushed into the box.
    # Object1 is bendable, so it is bent before being picked and placed into the box.
    # The sequence respects the constraints: compressible objects are pushed, and bendable objects are bent before placement.

    # Finally, add this code    
    print("All task planning is done")

