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
    is_foldable: bool = False
    is_plastic: bool = False

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
        # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # State the effect of Action: update the robot's state to holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint should be considered
        if obj.is_plastic and any(o.is_compressible for o in box.in_bin_objects):
            print(f"place {obj.name}")
            # Update the state to reflect the object being placed
            self.state_handempty()
            box.in_bin_objects.append(obj)
            obj.in_bin = True
        elif not obj.is_plastic:
            print(f"place {obj.name}")
            # Update the state to reflect the object being placed
            self.state_handempty()
            box.in_bin_objects.append(obj)
            obj.in_bin = True
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Ensure the robot hand is empty after pushing
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Ensure the robot's hand is empty before folding
            self.state_handempty()
            # No change in holding state as folding does not require holding the object
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_compressible is True, actions pick, place, push are applicable
    # object1: is_compressible is True, actions pick, place, push are applicable
    # object2: is_foldable is True, actions pick, place, fold are applicable
    # object3: is_plastic is True, actions pick, place are applicable
    # object4: is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place all compressible objects first, then push them.
    # 2. Fold the foldable object before placing it.
    # 3. Finally, place the plastic object after a compressible object is in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Handle compressible objects
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Handle foldable object
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    # Handle plastic object
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts by placing compressible objects first, ensuring that the rule of pushing them after placement is followed.
    # The foldable object is folded before being picked and placed, adhering to the rule for foldable objects.
    # The plastic object is placed last, ensuring a compressible object is already in the box, satisfying the constraint for plastic objects.

    # Finally, add this code    
    print("All task planning is done")
