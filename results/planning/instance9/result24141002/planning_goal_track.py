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
    is_plastic: bool = False
    is_rigid: bool = False
    is_foldable: bool = False
    is_bendable: bool = False

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
        # Preconditions: The object should not be in the box, and the robot's hand should be empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the object is considered in the robot's hand
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
    # Check if the object is plastic and if the constraint should be considered
    if obj.is_plastic and (obj.is_foldable or obj.is_bendable):
        # Check if there is a compressible object already in the box
        compressible_in_box = any(o.is_foldable or o.is_bendable for o in box.in_bin_objects)
        if not compressible_in_box:
            print(f"Cannot place {obj.name}")
            return

    # Action Description: Place an object into the box. This action can be applied to any type of object.
    print(f"place {obj.name}")
    # Update the state to reflect the object is now in the box
    obj.in_bin = True
    box.in_bin_objects.append(obj)
    self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # State the effect of Action: hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            # Preconditions: Hand must be empty
            if self.robot_handempty:
                # Action Description: Fold the object
                print(f"fold {obj.name}")
                # Effects: Hand remains empty after folding
                self.state_handempty()
            else:
                print(f"Cannot fold {obj.name} because the hand is not empty")
        else:
            print(f"Cannot fold {obj.name} due to constraints")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_plastic is True, actions pick, place are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_foldable is True, actions pick, place, fold are applicable
    # the object3.is_bendable is True, actions pick, place, bend are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume or change the physical properties of the object.
    # Write here.
    # 1. Bend object3 (black_1D_line) before placing it.
    # 2. Fold object2 (transparent_2D_circle) before placing it.
    # 3. Place object2 in the box.
    # 4. Place object3 in the box.
    # 5. Place object1 (blue_3D_cylinder) in the box.
    # 6. Place object0 (red_3D_cuboid) in the box, ensuring a compressible object is already in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)  # Bend the bendable object
    action.fold(object2, box)  # Fold the foldable object
    action.pick(object2, box)  # Pick the foldable object
    action.place(object2, box) # Place the foldable object
    action.pick(object3, box)  # Pick the bendable object
    action.place(object3, box) # Place the bendable object
    action.pick(object1, box)  # Pick the rigid object
    action.place(object1, box) # Place the rigid object
    action.pick(object0, box)  # Pick the plastic object
    action.place(object0, box) # Place the plastic object

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before placing the respective objects.
    # Object2 (foldable) is placed first to satisfy the condition for placing the plastic object (object0).
    # Object3 (bendable) is bent before being placed.
    # Object1 (rigid) is placed without additional constraints.
    # Object0 (plastic) is placed last, ensuring a compressible object is already in the box.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
