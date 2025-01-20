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
    is_rigid: bool = False
    is_compressible: bool = False
    is_foldable: bool = False
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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and its hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic:
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # If constraints are satisfied or not applicable, place the object
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

    def push(self, obj, box):
        # Check preconditions: object must be compressible and not plastic
        if obj.is_compressible and not obj.is_plastic and not self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effect: The robot's hand remains empty after pushing
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. The robot must be holding the object.
        # Preconditions: The object must be foldable and the robot must be holding it.
        if obj.is_foldable and not self.robot_handempty:
            print(f"fold {obj.name}")
            # Effects: The robot's hand remains holding the object after folding.
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True, is_2D=True)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True, is_2D=True)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True, is_2D=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid=True, actions pick, place are applicable
    # object1: is_plastic=True, is_2D=True, actions pick, place are applicable (requires compressible object in box first)
    # object2: is_foldable=True, is_2D=True, actions pick, place, fold are applicable
    # object3: is_foldable=True, is_2D=True, actions pick, place, fold are applicable
    # object4: is_compressible=True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick object4 (compressible), place it in the box, then push it.
    # 2. Pick object2 (foldable), fold it, then place it in the box.
    # 3. Pick object3 (foldable), fold it, then place it in the box.
    # 4. Pick object1 (plastic), place it in the box (after object4 is in the box).
    # 5. Pick object0 (rigid), place it in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object2, box)
    action.fold(object2, box)
    action.place(object2, box)

    action.pick(object3, box)
    action.fold(object3, box)
    action.place(object3, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence ensures that all objects are placed in the box following the given rules.
    # Object4 is placed first because it is compressible, allowing object1 (plastic) to be placed afterward.
    # Objects2 and 3 are foldable, so they are folded before being placed.
    # Object0 is rigid and can be placed without additional constraints.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
