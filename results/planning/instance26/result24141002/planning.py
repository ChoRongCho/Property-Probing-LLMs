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
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint should be applied
        if obj.is_plastic:
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return

        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        
        # State the effect of Action
        self.state_handempty()  # Assuming the robot hand becomes empty after placing the object
        obj.in_bin = True
        box.in_bin_objects.append(obj)

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            # Preconditions: Hand must be empty before pushing
            if self.robot_handempty:
                print(f"push {obj.name}")
                # Effects: Hand remains empty after pushing
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name}: Hand is not empty")
        else:
            # If the object is not compressible or is plastic, ignore constraints
            print(f"push {obj.name}")
            # Effects: Hand remains empty after pushing
            self.state_handempty()

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if hasattr(obj, 'is_foldable') and obj.is_foldable and hasattr(obj, 'is_plastic') and not obj.is_plastic:
            # Preconditions: The robot's hand must be empty to fold the object
            if self.robot_handempty:
                print(f"fold {obj.name}")
                # Effects: The robot's hand remains empty after folding
                self.state_handempty()
            else:
                print(f"Cannot fold {obj.name} because the robot's hand is not empty")
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
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_foldable is True, actions pick, place, fold are applicable
    # object3.is_plastic is True, actions pick, place are applicable
    # object4.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object2 (foldable) before picking and placing it.
    # 2. Pick and place object0 (compressible), then push it.
    # 3. Pick and place object1 (compressible), then push it.
    # 4. Pick and place object4 (compressible), then push it.
    # 5. Pick and place object3 (plastic) after a compressible object is in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)  # Fold object2
    action.pick(object2, box)  # Pick object2
    action.place(object2, box)  # Place object2

    action.pick(object0, box)  # Pick object0
    action.place(object0, box)  # Place object0
    action.push(object0, box)  # Push object0

    action.pick(object1, box)  # Pick object1
    action.place(object1, box)  # Place object1
    action.push(object1, box)  # Push object1

    action.pick(object4, box)  # Pick object4
    action.place(object4, box)  # Place object4
    action.push(object4, box)  # Push object4

    action.pick(object3, box)  # Pick object3
    action.place(object3, box)  # Place object3

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, ensure a compressible object is in the box before placing the plastic object, and push all compressible objects after placing them. This ensures all objects are packed according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")
