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
    is_foldable: bool
    is_compressible: bool

    # Additional predicates for bin_packing (max: 1)
    is_3D: bool


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
        # Preconditions: The object must not be in the bin, and the robot hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic and obj.is_compressible:
            # Check if there is already a compressible object in the box
            if any(o.is_compressible for o in box.in_bin_objects):
                print(f"place {obj.name}")
                # Effect: Update the state to reflect the object is now in the box
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name} - no compressible object in the box")
        else:
            # If the object is not plastic or the constraint does not apply, place it directly
            print(f"place {obj.name}")
            # Effect: Update the state to reflect the object is now in the box
            self.state_handempty()
            box.in_bin_objects.append(obj)

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and 3D, and not plastic
        if obj.is_compressible and obj.is_3D and not obj.is_plastic:
            # Preconditions: Hand must be empty to push
            if self.robot_handempty:
                print(f"push {obj.name}")
                # Effects: Hand remains empty after pushing
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name}, hand is not empty")
        else:
            print(f"Cannot push {obj.name}, does not meet constraints")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if hasattr(obj, 'is_foldable') and obj.is_foldable and hasattr(obj, 'is_plastic') and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            if self.robot_handempty:
                print(f"fold {obj.name}")
                # State the effect of Action: Hand remains empty after folding
                self.state_handempty()
            else:
                print(f"Cannot fold {obj.name}, hand is not empty")
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_foldable=False, is_compressible=False, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_foldable=False, is_compressible=False, is_3D=False)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=False, is_rigid=False, is_foldable=True, is_compressible=False, is_3D=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=False, is_foldable=False, is_compressible=True, is_3D=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_foldable=False, is_compressible=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0 is plastic and 3D, actions pick, place are applicable
    # object1 is plastic and 2D, actions pick, place are applicable
    # object2 is foldable and 2D, actions pick, place, fold are applicable
    # object3 is compressible and 3D, actions pick, place, push are applicable
    # object4 is rigid and 3D, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick object3 (compressible), place it, and push it.
    # 2. Fold object2 (foldable), pick it, and place it.
    # 3. Pick object4 (rigid), place it.
    # 4. Pick object0 (plastic), place it (after object3 is in the box).
    # 5. Pick object1 (plastic), place it (after object3 is in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object4, box)
    action.place(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts with placing a compressible object (object3) to satisfy the rule for placing plastic objects later.
    # Object2 is foldable, so it is folded before being picked and placed.
    # Object4 is rigid and can be placed without any additional actions.
    # Object0 and object1 are plastic, and they are placed after object3 is already in the box, satisfying the rule for plastic objects.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
