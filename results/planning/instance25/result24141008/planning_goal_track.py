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
    is_compressible: bool
    is_bendable: bool
    
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
        # Preconditions: The robot's hand must be empty, and the object must not already be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the object is considered in the robot's possession.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is holding the object and the object is not already in a bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Check if the object is a box or an object
            if obj.object_type == "obj":
                # Check if the object is compressible if the constraint applies
                if obj.is_compressible or obj.object_type != "plastic":
                    print(f"place {obj.name}")
                    # Update the state to reflect the object is placed in the bin
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} due to constraints")
            else:
                print(f"place {obj.name}")
                # Update the state to reflect the object is placed in the bin
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Check if the object is bendable
        if obj.is_bendable:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # State the effect of Action: Ensure the hand is empty before and after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check preconditions: The object must be compressible and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
            # Effect: The robot's hand remains empty after pushing.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_bendable=False, is_heavy=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_bendable=False, is_heavy=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_bendable=True, is_heavy=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_bendable=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_compressible is True, actions pick, place, push are applicable
    # object1: is_rigid is True, actions pick, place are applicable
    # object2: is_bendable is True, actions pick, place, bend are applicable
    # object3: is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it is bendable.
    # 2. Pick and place object2 into the box.
    # 3. Pick and place object0 (yellow_3D_cuboid) into the box, then push it.
    # 4. Pick and place object1 (blue_3D_cylinder) into the box.
    # 5. Pick and place object3 (green_3D_cylinder) into the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)  # Bend the bendable object
    action.pick(object2, box)  # Pick the bendable object
    action.place(object2, box)  # Place the bendable object in the box

    action.pick(object0, box)  # Pick the compressible object
    action.place(object0, box)  # Place the compressible object in the box
    action.push(object0, box)  # Push the compressible object

    action.pick(object1, box)  # Pick the rigid object
    action.place(object1, box)  # Place the rigid object in the box

    action.pick(object3, box)  # Pick the rigid object
    action.place(object3, box)  # Place the rigid object in the box

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing, place a compressible object before any plastic object,
    # and push compressible objects after placing them. Non-plastic objects are placed without additional constraints.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
