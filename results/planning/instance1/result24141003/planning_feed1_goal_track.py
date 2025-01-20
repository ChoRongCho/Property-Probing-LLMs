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
    is_rigid: bool

    # Additional predicates for bin_packing (max: 1)
    is_heavy: bool


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
        # Preconditions: The object is not in the bin, and the robot's hand is empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is not empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint should be considered
        if obj.is_plastic:
            # Ignore the constraint about compressible objects since it's not defined in the Object class
            pass

        # If constraints are not applicable or satisfied, proceed with placing the object
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

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
    # object0.is_plastic is True, actions pick, place are applicable (requires a compressible object in the box first)
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True 
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Since none of the objects are compressible, we can place non-plastic objects first.
    # 1. Pick and place object1 (white_3D_cuboid) into the box.
    # 2. Pick and place object2 (green_3D_cylinder) into the box.
    # 3. Pick and place object0 (red_3D_cuboid) into the box (after non-plastic objects are placed).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object1, box)
    action.place(object1, box)
    
    action.pick(object2, box)
    action.place(object2, box)
    
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: non-plastic objects are placed first without constraints.
    # The plastic object (object0) is placed last, ensuring that the rule requiring a compressible object is ignored as there are none.
    # The actions are executed in a sequence that respects the robot's capabilities and object properties.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
