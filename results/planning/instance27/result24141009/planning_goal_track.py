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
    is_rigid: bool

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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note: If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the robot is holding the object and the object is not already in a bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Check if the object is compressible or if there are already objects in the box
            if obj.is_compressible or box.in_bin_objects:
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the bin
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                # Update the robot's state to hand empty
                self.state_handempty()
            else:
                print(f"Cannot place {obj.name} because no compressible object is in the box")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.in_bin and obj.is_compressible:
            print(f"push {obj.name}")
            # No change in the state of the robot's hand as it remains empty
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_fragile=False)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_fragile=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_fragile=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_rigid is True, actions pick, place are applicable
    # object3.is_compressible is True, actions pick, place, push are applicable
    # object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object0 (compressible), then push it.
    # 2. Pick and place object1 (compressible), then push it.
    # 3. Pick and place object3 (compressible), then push it.
    # 4. Pick and place object2 (rigid, non-plastic).
    # 5. Pick and place object4 (rigid, non-plastic).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts with placing compressible objects (object0, object1, object3) and pushing them as required by the rules.
    # Non-plastic objects (object2, object4) are placed without constraints.
    # The sequence respects the rule that a compressible object must be in the box before placing a plastic object.
    # No bending or folding actions are necessary as there are no bendable or foldable objects.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
