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
    is_foldable: bool = False
    is_rigid: bool = False
    is_bendable: bool = False
    is_plastic: bool = False

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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and its hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint is applicable
        if obj.is_plastic:
            # Check if there is a compressible object already in the box
            compressible_present = any(o.is_foldable or o.is_bendable for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state to hand empty after placing the object
        self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            if self.robot_handempty:
                print(f"bend {obj.name}")
                # No change in hand state since the hand remains empty
                self.state_handempty()
            else:
                print(f"Cannot bend {obj.name} because the hand is not empty")
        else:
            print(f"Cannot bend {obj.name} because it is either not bendable or is plastic")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        # Action Description: Fold a foldable object. Hand must remain empty before and after the folding.
        # Preconditions: The object must be foldable, and the robot's hand must be empty.
        if obj.is_foldable and self.robot_handempty:
            print(f"fold {obj.name}")
            # Effects: The robot's hand remains empty after folding.
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_foldable is True, actions pick, place, fold are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_bendable is True, actions pick, place, bend are applicable
    # object3.is_plastic is True, actions pick, place are applicable (with constraints)

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 (yellow_2D_rectangle) -> Pick object0 -> Place object0 -> Push object0
    # 2. Bend object2 (black_1D_line) -> Pick object2 -> Place object2 -> Push object2
    # 3. Pick object1 (beige_1D_line) -> Place object1
    # 4. Pick object3 (gray_1D_line) -> Place object3 (since object0 or object2 is already in the box)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object0, box)
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before picking and placing,
    # ensuring that compressible objects are pushed after placement. The plastic object is placed last,
    # ensuring a compressible object is already in the box to satisfy the constraint.

    # Finally, add this code    
    print("All task planning is done")
