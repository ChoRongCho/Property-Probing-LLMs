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
    is_placed: bool = False


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
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check preconditions
        if self.robot_handempty and not obj.is_placed:
            # Check constraints for placing a plastic object
            if obj.is_plastic:
                # Ensure there is at least one compressible object in the box
                compressible_present = any(o.is_foldable for o in box.in_bin_objects)
                if not compressible_present:
                    print(f"Cannot place {obj.name}")
                    return
            
            # Action Description: Place an object into the box. This action can be applied to any type of object.
            print(f"place {obj.name}")
            # Update the state to reflect the object is now placed
            obj.is_placed = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # State the effect of Action: Ensure the robot's hand is empty after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        # Check if the object is foldable and the robot's hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Action Description: Fold a foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Since the hand must remain empty, no change in hand state is needed
            # No additional effects on the box are specified for folding
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True, is_rigid=False, is_bendable=False, is_plastic=False, is_placed=False)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_foldable=False, is_rigid=True, is_bendable=False, is_plastic=False, is_placed=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_foldable=False, is_rigid=False, is_bendable=True, is_plastic=False, is_placed=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_foldable=False, is_rigid=False, is_bendable=False, is_plastic=True, is_placed=False)

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
    # 1. Fold object0 (foldable)
    # 2. Pick object0
    # 3. Place object0
    # 4. Push object0 (compressible)
    # 5. Bend object2 (bendable)
    # 6. Pick object2
    # 7. Place object2
    # 8. Pick object1
    # 9. Place object1
    # 10. Pick object3 (plastic, ensure compressible object is in box)
    # 11. Place object3

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object0, box)
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: foldable objects are folded before being picked and placed.
    # Bendable objects are bent before being picked and placed. Compressible objects are pushed after being placed.
    # The plastic object is placed only after a compressible object is in the box, satisfying the constraints.

    # Finally, add this code    
    print("All task planning is done")
