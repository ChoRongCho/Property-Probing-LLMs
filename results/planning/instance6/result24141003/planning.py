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
    is_foldable: bool
    is_compressible: bool

    # Additional predicates for bin_packing (max: 1)
    is_heavy: bool


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
            # Effects: The robot is now holding the object, and the hand is not empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic and obj.is_compressible:
            # Check if there is already a compressible object in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update robot state to hand empty after placing the object
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            # Preconditions: Hand must be empty and the object must be in the bin
            if self.robot_handempty and obj.in_bin:
                # Action Description: Push a 3D compressible object downward in the bin.
                print(f"push {obj.name}")
                # Effects: Hand remains empty after pushing
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name} because preconditions are not met")
        else:
            # If the object is not compressible or is plastic, ignore constraints and do not push
            print(f"Cannot push {obj.name} due to constraints")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if hasattr(obj, 'is_foldable') and obj.is_foldable and hasattr(obj, 'is_plastic') and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_foldable=False, is_compressible=False, is_heavy=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=False, is_foldable=False, is_compressible=True, is_heavy=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_foldable=False, is_compressible=True, is_heavy=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=False, is_foldable=True, is_compressible=False, is_heavy=False)
object4 = Object(index=4, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True, is_foldable=False, is_compressible=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0 is plastic and not compressible, actions pick, place are applicable
    # object1 is compressible and not plastic, actions pick, place, push are applicable
    # object2 is compressible and not plastic, actions pick, place, push are applicable
    # object3 is foldable and not plastic, actions pick, place, fold are applicable
    # object4 is plastic and not compressible, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and push compressible objects first (object1, object2)
    # 2. Fold foldable objects before placing (object3)
    # 3. Place plastic objects after a compressible object is in the box (object0, object4)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Pick, place, and push object1
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    # Pick, place, and push object2
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    # Fold and place object3
    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    # Place object0 (plastic, after a compressible object is in the box)
    action.pick(object0, box)
    action.place(object0, box)

    # Place object4 (plastic, after a compressible object is in the box)
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence ensures that all rules are followed: compressible objects are pushed after placing,
    # foldable objects are folded before placing, and plastic objects are placed only after a compressible
    # object is in the box. This ensures all objects reach their goal state of being in the bin.

    # Finally, add this code    
    print("All task planning is done")
