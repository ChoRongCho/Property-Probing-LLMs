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
    is_foldable: bool = False
    is_rigid: bool = False
    is_bendable: bool = False
    is_compressible: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_2D: bool = False
    is_1D: bool = False
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
        # Preconditions: The robot's hand must be empty, and the object must not be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if a compressible object is already in the box
        if obj.is_plastic:
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
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
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and obj.is_bendable and not obj.is_plastic:
            print(f"bend {obj.name}")
            # State the effect of Action: hand remains empty after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Check preconditions: object must be compressible and not plastic
        if obj.is_compressible and not obj.is_plastic and self.robot_handempty:
            # Action Description: Push a compressible object downward in the bin.
            print(f"push {obj.name}")
            # Effects: Hand remains empty after pushing
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            # Action Description: Fold a foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Assuming the robot's hand should be empty before and after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True, is_2D=True)
object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True, is_2D=True)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True, is_1D=True)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True, is_1D=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_plastic is True, actions pick, place are applicable
    # object1.is_foldable is True, actions pick, place, fold are applicable
    # object2.is_rigid is True, actions pick, place are applicable
    # object3.is_bendable is True, actions pick, place, bend are applicable
    # object4.is_compressible is True, actions pick, place, push are applicable
    # object5.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (black_1D_line) before placing.
    # 2. Fold object1 (transparent_2D_circle) before placing.
    # 3. Place object4 (brown_3D_cylinder) first as it is compressible.
    # 4. Push object4 after placing.
    # 5. Place object0 (blue_2D_rectangle) after a compressible object is in the box.
    # 6. Place remaining objects: object1, object2, object3, object5.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)  # Bend black_1D_line
    action.fold(object1, box)  # Fold transparent_2D_circle
    action.pick(object4, box)  # Pick brown_3D_cylinder
    action.place(object4, box) # Place brown_3D_cylinder
    action.push(object4, box)  # Push brown_3D_cylinder
    action.pick(object0, box)  # Pick blue_2D_rectangle
    action.place(object0, box) # Place blue_2D_rectangle
    action.pick(object1, box)  # Pick transparent_2D_circle
    action.place(object1, box) # Place transparent_2D_circle
    action.pick(object2, box)  # Pick beige_1D_line
    action.place(object2, box) # Place beige_1D_line
    action.pick(object3, box)  # Pick black_1D_line
    action.place(object3, box) # Place black_1D_line
    action.pick(object5, box)  # Pick green_3D_cylinder
    action.place(object5, box) # Place green_3D_cylinder

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before picking and placing.
    # A compressible object is placed first to allow placing of the plastic object.
    # The push action is performed immediately after placing the compressible object.
    # All objects are placed in the box, achieving the goal state.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4, object5]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
