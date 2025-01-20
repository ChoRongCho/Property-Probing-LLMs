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
    is_compressible: bool
    is_bendable: bool

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
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.

        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return

        # Check if the object is a plastic object and ensure a compressible object is already in the box
        # Since the constraint mentions "plastic" and there's no attribute for material type, ignore this constraint
        # Proceed with placing the object

        # Preconditions: The robot must be holding the object
        if self.robot_now_holding == obj:
            # Place the object in the box
            print(f"place {obj.name}")
            obj.in_bin = True
            box.in_bin_objects.append(obj)

            # Effects: Update the robot's state to hand empty
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}, the robot is not holding it.")

    def bend(self, obj, box):
        # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and obj.is_bendable:
            print(f"bend {obj.name}")
            # Effect: The object is bent, but since there's no state change in the Object class, no further effects are needed.
            # Ensure the robot's hand remains empty after the action
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.in_bin and obj.is_compressible:
            print(f"push {obj.name}")
            # No change in hand state since the hand remains empty before and after the push
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_fragile=False)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_bendable=True, is_fragile=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_fragile=False)

box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_bendable is True, actions pick, place, bend are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object1 (black_1D_line) since it is bendable.
    # 2. Pick and place object1 (black_1D_line) into the box.
    # 3. Pick and place object0 (white_3D_cylinder) into the box, then push it.
    # 4. Pick and place object2 (red_3D_polyhedron) into the box, then push it.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object1, box)  # Bend the bendable object
    action.pick(object1, box)  # Pick object1
    action.place(object1, box)  # Place object1 in the box

    action.pick(object0, box)  # Pick object0
    action.place(object0, box)  # Place object0 in the box
    action.push(object0, box)  # Push the compressible object0

    action.pick(object2, box)  # Pick object2
    action.place(object2, box)  # Place object2 in the box
    action.push(object2, box)  # Push the compressible object2

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing it, ensure a compressible object is in the box before placing any plastic object (though no plastic constraint is explicitly given), and push compressible objects after placing them. The sequence ensures all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
