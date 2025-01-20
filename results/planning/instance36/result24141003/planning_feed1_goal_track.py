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
    is_packable: bool = True


@dataclass
class Box:
    # Basic dataclass
    index: int
    name: str

    # Predicates for box
    object_type: str  # box or obj
    in_bin_objects: list

# only write a code here without example instantiation
# Note! If a predicate required by the constraints is not defined in the class Object, ignore the constraints!!!
class Action:
    def __init__(self, name: str = "UR5"):
        self.name = name    
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The object must not be in the bin, the robot hand must be empty, and the object must be packable.
        if not obj.in_bin and self.robot_handempty and obj.is_packable:
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The object must be packable, the robot must be holding the object, and if the object is plastic,
        # a compressible object must already be in the box.
        if obj.is_packable and self.robot_now_holding == obj:
            if obj.is_plastic:
                compressible_present = any(o.is_foldable or o.is_bendable for o in box.in_bin_objects)
                if not compressible_present:
                    print(f"Cannot place {obj.name}")
                    return
            
            # Effects: Place the object in the box, mark it as in_bin, and set the robot hand to empty.
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # State the effect of Action: Hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Check if the object is compressible (foldable or bendable) and not plastic
        if (obj.is_foldable or obj.is_bendable) and not obj.is_plastic:
            print(f"push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and the robot's hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # No change in the robot's state since the hand remains empty before and after folding
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True, is_packable=True)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True, is_packable=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True, is_packable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True, is_packable=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_foldable is True, actions pick, place, fold are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_bendable is True, actions pick, place, bend are applicable
    # object3.is_plastic is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 before placing it.
    # 2. Bend object2 before placing it.
    # 3. Place object0 in the box.
    # 4. Place object2 in the box.
    # 5. Push object0 and object2 after placing them.
    # 6. Place object1 in the box.
    # 7. Place object3 in the box (after a compressible object is in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object0, box)  # Fold object0
    action.pick(object0, box)  # Pick object0
    action.place(object0, box)  # Place object0
    action.push(object0, box)  # Push object0

    action.bend(object2, box)  # Bend object2
    action.pick(object2, box)  # Pick object2
    action.place(object2, box)  # Place object2
    action.push(object2, box)  # Push object2

    action.pick(object1, box)  # Pick object1
    action.place(object1, box)  # Place object1

    action.pick(object3, box)  # Pick object3
    action.place(object3, box)  # Place object3

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before placing foldable and bendable objects.
    # Compressible objects are pushed after being placed. The plastic object is placed after a compressible object is in the box.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
