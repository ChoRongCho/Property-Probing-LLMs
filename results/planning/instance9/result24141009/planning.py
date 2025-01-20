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
    is_3D: bool = False


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
        # Preconditions: The object must not be in the bin and the robot's hand must be empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic:
            # Check if there's a compressible object already in the box
            compressible_present = any(o.is_foldable or o.is_bendable for o in box.in_bin_objects)
            
            if compressible_present:
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the box
                self.state_handempty()
                obj.in_bin = True
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # Non-plastic objects can be placed without constraints
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            self.state_handempty()
            obj.in_bin = True
            box.in_bin_objects.append(obj)

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if hasattr(obj, 'is_bendable') and obj.is_bendable and hasattr(obj, 'is_plastic') and not obj.is_plastic:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            if self.robot_handempty:
                print(f"bend {obj.name}")
                # State the effect of Action: hand remains empty
                self.state_handempty()
            else:
                print(f"Cannot bend {obj.name}, hand is not empty")
        else:
            print(f"Cannot bend {obj.name}, it is either not bendable or is plastic")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is foldable, not plastic, and is 2D
        if hasattr(obj, 'is_foldable') and obj.is_foldable and not obj.is_3D and not obj.is_plastic:
            print(f"fold {obj.name}")
            # Assuming the robot's hand must be empty before and after folding
            self.state_handempty()
            # No change in the state of the robot's hand since folding does not require holding the object
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_3D=True)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_plastic is True, actions pick, place are applicable (with constraint)
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_foldable is True, actions pick, place, fold are applicable
    # object3.is_bendable is True, actions pick, place, bend are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (black_1D_line) before placing it in the box.
    # 2. Fold object2 (transparent_2D_circle) before placing it in the box.
    # 3. Place object3 (black_1D_line) in the box.
    # 4. Place object2 (transparent_2D_circle) in the box.
    # 5. Place object1 (blue_3D_cylinder) in the box.
    # 6. Place object0 (red_3D_cuboid) in the box (after a compressible object is in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)  # Bend the bendable object
    action.pick(object3, box)
    action.place(object3, box)  # Place the bendable object in the box

    action.fold(object2, box)  # Fold the foldable object
    action.pick(object2, box)
    action.place(object2, box)  # Place the foldable object in the box

    action.pick(object1, box)
    action.place(object1, box)  # Place the rigid object in the box

    action.pick(object0, box)
    action.place(object0, box)  # Place the plastic object in the box

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before placing bendable and foldable objects.
    # A compressible object (object2) is placed in the box before placing the plastic object (object0).
    # The robot's hand is empty before and after bend, fold, and push actions, as required.

    # Finally, add this code    
    print("All task planning is done")
