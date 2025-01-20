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
    is_rigid: bool
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
        # Preconditions: The object must not be in a box and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and ensure a compressible object is already in the box
        if obj.is_plastic:
            if any(o.is_compressible for o in box.in_bin_objects):
                print(f"place {obj.name}")
                self.state_handempty()  # Assuming placing an object leaves the hand empty
                box.in_bin_objects.append(obj)
                obj.in_bin = True
            else:
                print(f"Cannot place {obj.name}")
        else:
            # Non-plastic objects can be placed without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Assuming placing an object leaves the hand empty
            box.in_bin_objects.append(obj)
            obj.in_bin = True

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Preconditions: The object must be compressible and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after the push.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable
        if obj.is_foldable:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            if self.robot_handempty:
                print(f"fold {obj.name}")
                # State the effect of Action: Hand remains empty after folding
                self.state_handempty()
            else:
                print(f"Cannot fold {obj.name} because the hand is not empty")
        else:
            print(f"Cannot fold {obj.name} because it is not foldable")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=False, is_plastic=True, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_plastic=False, is_fragile=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=True, is_plastic=False, is_fragile=False)
object3 = Object(index=3, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_foldable=False, is_plastic=False, is_fragile=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_plastic=False, is_fragile=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_foldable=False, is_plastic=False, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_plastic is True, actions pick, place are applicable
    # object1: is_compressible is True, actions pick, place, push are applicable
    # object2: is_foldable is True, actions pick, place, fold are applicable
    # object3: is_rigid is True, actions pick, place are applicable
    # object4: is_compressible is True, actions pick, place, push are applicable
    # object5: is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object2 (foldable) before placing.
    # 2. Pick and place object1 (compressible) and then push it.
    # 3. Pick and place object4 (compressible) and then push it.
    # 4. Pick and place object0 (plastic) after a compressible object is in the box.
    # 5. Pick and place object3 (rigid).
    # 6. Pick and place object5 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, ensure a compressible object is in the box before placing a plastic object, and push compressible objects after placing them. Non-plastic, non-compressible objects are placed without additional actions.

    # Finally, add this code    
    print("All task planning is done")
