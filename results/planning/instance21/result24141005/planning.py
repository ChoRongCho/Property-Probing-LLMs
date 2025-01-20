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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and its hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint is applicable
        if obj.is_plastic:
            # Check if there is at least one compressible object already in the box
            compressible_present = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return

        # If constraints are satisfied or not applicable, place the object
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check preconditions: object must be compressible and 3D, and the robot's hand must be empty
        if obj.is_compressible and obj.is_3D and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin. 
            print(f"push {obj.name}")
            # Effect: The robot's hand remains empty after pushing
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and not obj.is_3D and obj.is_foldable:
            print(f"fold {obj.name}")
            # State the effect of Action and box: self.state_holding or self.state_handempty etc if necessary
            self.state_handempty()  # Ensure the hand remains empty after folding
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_rigid is True and object0.is_3D is True, actions pick, place are applicable
    # the object1.is_plastic is True, actions pick, place are applicable
    # the object2.is_foldable is True, actions pick, place, fold are applicable
    # the object3.is_foldable is True, actions pick, place, fold are applicable
    # the object4.is_compressible is True and object4.is_3D is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object4 (compressible) into the box, then push it.
    # 2. Pick, fold, and place object2 (foldable) into the box.
    # 3. Pick, fold, and place object3 (foldable) into the box.
    # 4. Pick and place object0 (rigid) into the box.
    # 5. Pick and place object1 (plastic) into the box, since object4 (compressible) is already in the box.

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

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: object4 is placed and pushed first to allow object1 (plastic) to be placed later.
    # Foldable objects (object2 and object3) are folded before placing. Object0 is placed without constraints.
    # The sequence ensures all objects are packed as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
