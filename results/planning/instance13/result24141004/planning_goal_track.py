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
    is_compressible: bool = False

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
        # Preconditions: The object must not be in the bin, and the robot hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic:
            # Check if there is at least one compressible object already in the box
            if any(o.is_compressible for o in box.in_bin_objects):
                # Preconditions are satisfied, proceed to place the object
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the box
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                self.state_handempty()
            else:
                # Constraint not satisfied, cannot place the object
                print(f"Cannot place {obj.name} due to missing compressible object")
        else:
            # Non-plastic objects can be placed without constraints
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and 3D, and not plastic
        if obj.is_compressible and obj.is_3D and not obj.is_plastic:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Ensure the robot's hand is empty after the action
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if obj.is_foldable and not obj.is_plastic:
            print(f"fold {obj.name}")
            # Effect: The robot's hand remains empty before and after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_plastic is True, object0.is_3D is True, actions pick, place are applicable
    # object1.is_plastic is True, actions pick, place are applicable
    # object2.is_foldable is True, actions pick, place, fold are applicable
    # object3.is_compressible is True, object3.is_3D is True, actions pick, place, push are applicable
    # object4.is_rigid is True, object4.is_3D is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object3 (compressible) first, then push it.
    # 2. Fold object2 (foldable), then pick and place it.
    # 3. Pick and place object0 (plastic) after object3 is in the box.
    # 4. Pick and place object1 (plastic) after object3 is in the box.
    # 5. Pick and place object4 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts with placing the compressible object (object3) to satisfy the constraint for placing plastic objects.
    # Object2 is folded before placing, as required by its foldable property.
    # Plastic objects (object0 and object1) are placed after object3 to meet the constraint.
    # Object4 is rigid and can be placed without additional actions.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
