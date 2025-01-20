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

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The robot's hand must be empty, and the object must not be in a bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note: If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return
        
        # Check if the robot is holding the object
        if not self.robot_now_holding:
            print(f"Cannot place {obj.name}, the robot is not holding the object.")
            return
        
        # Check if the object is a box or an object
        if obj.object_type == "obj":
            # Check if the object is fragile and ensure it is not placed at the bottom
            if obj.is_fragile and len(box.in_bin_objects) == 0:
                print(f"Cannot place {obj.name}, it is fragile and cannot be placed at the bottom.")
                return
            
            # Place the object in the box
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"place {obj.name}")
        
        elif obj.object_type == "box":
            # Place the box in the bin
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"place {obj.name}")
        
        else:
            print(f"Cannot place {obj.name}, unknown object type.")

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        if self.robot_handempty and obj.is_bendable:
            print(f"bend {obj.name}")
            # State the effect of Action: hand remains empty after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.is_compressible and obj.in_bin:
            print(f"push {obj.name}")
            # Since the hand must remain empty before and after, no state change is needed
            self.state_handempty()
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
    # object0 is compressible, actions pick, place, push are applicable
    # object1 is bendable, actions pick, place, bend are applicable
    # object2 is compressible, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object0 (compressible) into the box, then push it.
    # 2. Bend object1 (bendable), then pick and place it into the box.
    # 3. Pick and place object2 (compressible) into the box, then push it.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

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
    # Object0 is compressible, so it can be placed first and pushed afterward.
    # Object1 is bendable, so it must be bent before placing it in the box.
    # Object2 is compressible, so it can be placed after object0 and pushed afterward.
    # The sequence respects the rules regarding compressible and bendable objects.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
