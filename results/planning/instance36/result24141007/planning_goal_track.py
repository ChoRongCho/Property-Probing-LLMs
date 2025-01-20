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
    is_2D: bool = False


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
        # Preconditions: The object must not be in the box, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return

        # Check if the object is plastic and if the constraint is applicable
        if obj.is_plastic:
            # Check if there's a compressible object already in the box
            compressible_present = any(o.is_foldable or o.is_bendable for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}, a compressible object must be in the box first.")
                return

        # Place the object in the box
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the bin
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        # Update the robot's state
        self.state_handempty()

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Note: If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Preconditions: The object must be bendable and the robot's hand must be empty.
        if obj.is_bendable and self.robot_handempty:
            print(f"bend {obj.name}")
            # Effects: The robot's hand remains empty after the action.
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            self.state_handempty()  # Ensure the hand is empty before folding
            print(f"fold {obj.name}")
            self.state_handempty()  # Ensure the hand is empty after folding
            # Additional effects can be added here if necessary
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True, is_2D=True)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_foldable is True, actions pick, place, fold are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_bendable is True, actions pick, place, bend are applicable
    # the object3.is_plastic is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume or change the physical properties of the object.
    # Order: object0 (fold, pick, place, push), object2 (bend, pick, place, push), object1 (pick, place), object3 (pick, place)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # For object0
    action.fold(object0, box)
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    # For object2
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    # For object1
    action.pick(object1, box)
    action.place(object1, box)

    # For object3
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Object0 is foldable, so it is folded before picking and placing in the box. After placing, it is pushed.
    # Object2 is bendable, so it is bent before picking and placing in the box. After placing, it is pushed.
    # Object1 is rigid, so it is directly picked and placed without additional actions.
    # Object3 is plastic, and since a compressible object (object0 or object2) is already in the box, it can be placed after picking.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
