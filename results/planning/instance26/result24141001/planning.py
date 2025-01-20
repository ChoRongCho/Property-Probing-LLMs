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
    is_foldable: bool
    is_plastic: bool

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
            # Effects: The robot is now holding the object, and its hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint should be applied
        if obj.is_plastic and obj.is_compressible:
            # Check if there is at least one compressible object already in the box
            if any(o.is_compressible for o in box.in_bin_objects):
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the box
                box.in_bin_objects.append(obj)
                self.state_handempty()
            else:
                print(f"Cannot place {obj.name}")
        else:
            # If the object is not plastic or the constraint is not applicable, place it
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            box.in_bin_objects.append(obj)
            self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Since the hand must remain empty, ensure the state reflects this
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if hasattr(obj, 'is_foldable') and obj.is_foldable and hasattr(obj, 'is_plastic') and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: Hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_foldable=False, is_plastic=False, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_foldable=False, is_plastic=False, is_fragile=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_compressible=False, is_foldable=True, is_plastic=False, is_fragile=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_foldable=False, is_plastic=True, is_fragile=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_foldable=False, is_plastic=False, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_compressible is True, actions pick, place, push are applicable
    # the object1.is_compressible is True, actions pick, place, push are applicable
    # the object2.is_foldable is True, actions pick, place, fold are applicable
    # the object3.is_plastic is True, actions pick, place are applicable
    # the object4.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object2 before placing it.
    # 2. Pick and place object0, then push it.
    # 3. Pick and place object1, then push it.
    # 4. Pick and place object4, then push it.
    # 5. Pick and place object3 (ensure a compressible object is already in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: foldable objects are folded before placing, compressible objects are pushed after placing,
    # and plastic objects are placed only after a compressible object is already in the box. The sequence ensures all objects
    # reach their goal state of being in the bin.

    # Finally, add this code    
    print("All task planning is done")
