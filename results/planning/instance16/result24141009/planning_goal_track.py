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
    is_rigid: bool = False
    is_compressible: bool = False
    is_foldable: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_heavy: bool = False


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
        # Preconditions: The robot's hand must be empty, and the object must not be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object can be placed based on constraints
        if obj.object_type == "plastic" and not any(o.is_compressible for o in box.in_bin_objects):
            # Constraint: A compressible object must be in the box before placing a plastic object
            print(f"Cannot place {obj.name}")
        else:
            # Action Description: Place an object into the box. This action can be applied to any type of object.
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            # Update robot state to hand empty after placing the object
            self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Preconditions: The object must be compressible and in the bin, and the robot's hand must be empty.
        if obj.is_compressible and obj.in_bin and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin. Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after the action.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable
        if obj.is_foldable:
            # Action Description: Fold a foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Since the action does not involve holding the object, the robot's state remains handempty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, actions pick, place are applicable
    # object1: is_compressible is True, actions pick, place, push are applicable
    # object2: is_compressible is True, actions pick, place, push are applicable
    # object3: is_foldable is True, actions pick, place, fold are applicable
    # object4: is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and fold object3 (foldable) before placing it.
    # 2. Pick and place object1 (compressible), then push it.
    # 3. Pick and place object2 (compressible), then push it.
    # 4. Pick and place object4 (compressible), then push it.
    # 5. Pick and place object0 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)  # Fold object3 before picking
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, place compressible objects first, and push them after placing. Finally, place the rigid object. This ensures all constraints are respected and all objects are packed as per the goal states.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
