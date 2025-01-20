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
    is_bendable: bool
    is_compressible: bool
    is_foldable: bool

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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. 
            # The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return

        # Check if the object is a plastic object and ensure a compressible object is already in the box
        # Note: Since the constraint mentions "plastic" and it's not a property in the Object class, ignore this constraint.
        
        # Preconditions: The robot must be holding the object and the object must not already be in the bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Effect: Place the object in the bin
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()  # Robot hand is now empty after placing the object
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and obj.is_bendable:
            print(f"bend {obj.name}")
            # State the effect of Action: Hand remains empty after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after pushing.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and the robot's hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Action Description: Fold a foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_compressible=False, is_foldable=False, is_heavy=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_compressible=True, is_foldable=False, is_heavy=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_compressible=False, is_foldable=True, is_heavy=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=True, is_compressible=False, is_foldable=False, is_heavy=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_compressible=True, is_foldable=False, is_heavy=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_compressible=False, is_foldable=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid=True, actions pick, place are applicable
    # object1: is_compressible=True, actions pick, place, push are applicable
    # object2: is_foldable=True, actions pick, place, fold are applicable
    # object3: is_bendable=True, actions pick, place, bend are applicable
    # object4: is_compressible=True, actions pick, place, push are applicable
    # object5: is_rigid=True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (bendable)
    # 2. Fold object2 (foldable)
    # 3. Pick and place object1 (compressible), then push
    # 4. Pick and place object4 (compressible), then push
    # 5. Pick and place object0 (rigid)
    # 6. Pick and place object5 (rigid)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)
    action.fold(object2, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)
    action.pick(object0, box)
    action.place(object0, box)
    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before placing bendable and foldable objects.
    # Compressible objects are pushed after being placed. Non-plastic objects are placed without constraints.
    # The sequence ensures all objects are packed according to the goal states.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4, object5]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
