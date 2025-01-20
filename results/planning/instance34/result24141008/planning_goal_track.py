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
        # Preconditions: The object must not be in the bin and the robot hand must be empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is currently holding the object
        if self.robot_now_holding == obj:
            # Check if the object is already in the bin
            if not obj.in_bin:
                # Check if the object is compressible or if the constraint is not applicable
                if obj.is_compressible or obj.object_type != "plastic":
                    print(f"place {obj.name}")
                    # Update the state to reflect the object is now in the bin
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                    # Update the robot's state to hand empty
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name}: Requires a compressible object in the box first")
            else:
                print(f"Cannot place {obj.name}: Already in the bin")
        else:
            print(f"Cannot place {obj.name}: Not currently holding the object")

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        if self.robot_handempty and obj.is_bendable:
            print(f"bend {obj.name}")
            # State the effect of Action: hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check preconditions: Object must be compressible and hand must be empty
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
            # Effect: Hand remains empty after the push
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
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_bendable is True, actions pick, place, bend are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object1 (black_1D_line) since it is bendable.
    # 2. Pick and place object1 into the box.
    # 3. Pick and place object0 (white_3D_cylinder) into the box, then push it since it is compressible.
    # 4. Pick and place object2 (red_3D_polyhedron) into the box, then push it since it is compressible.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object1, box)  # Bend the bendable object1
    action.pick(object1, box)  # Pick object1
    action.place(object1, box) # Place object1 into the box

    action.pick(object0, box)  # Pick object0
    action.place(object0, box) # Place object0 into the box
    action.push(object0, box)  # Push object0 since it is compressible

    action.pick(object2, box)  # Pick object2
    action.place(object2, box) # Place object2 into the box
    action.push(object2, box)  # Push object2 since it is compressible

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing, place compressible objects and then push them.
    # All objects are placed in the box as per the goal states, respecting the constraints for each object's properties.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
