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
        # Preconditions: The robot's hand must be empty, and the object must not be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object, and the object must not be in the bin.
        if not self.robot_handempty and obj == self.robot_now_holding:
            # Check if the object is of type 'obj' and if it is compressible
            if obj.object_type == 'obj':
                # Place the object in the box
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the bin
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                # Update the robot state to hand empty after placing the object
                self.state_handempty()
            else:
                print(f"Cannot place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Preconditions: Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.is_compressible and obj.in_bin:
            print(f"push {obj.name}")
            # Ensure the robot hand remains empty after the action
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable
        if obj.is_foldable:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: Hand remains empty after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_foldable=False, is_heavy=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_heavy=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_heavy=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=True, is_heavy=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid=True, is_compressible=False, is_foldable=False, actions: pick, place
    # object1: is_rigid=False, is_compressible=True, is_foldable=False, actions: pick, place, push
    # object2: is_rigid=False, is_compressible=True, is_foldable=False, actions: pick, place, push
    # object3: is_rigid=False, is_compressible=False, is_foldable=True, actions: pick, place, fold
    # object4: is_rigid=False, is_compressible=True, is_foldable=False, actions: pick, place, push

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object1 (compressible) into the box, then push it.
    # 2. Pick and place object2 (compressible) into the box, then push it.
    # 3. Fold object3 (foldable), pick and place it into the box.
    # 4. Pick and place object4 (compressible) into the box, then push it.
    # 5. Pick and place object0 (rigid) into the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: compressible objects are placed and pushed first, foldable objects are folded before placing,
    # and non-plastic objects are placed without additional constraints. The sequence ensures all objects reach their goal state.

    # Finally, add this code    
    print("All task planning is done")

