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
    is_rigid: bool
    is_bendable: bool

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
        # Preconditions: The object must not be in the box, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return

        # Check if the robot is holding the object
        if not self.robot_now_holding == obj:
            print(f"Cannot place {obj.name}, the robot is not holding it.")
            return

        # Check the constraint: Before placing a plastic object, a compressible object should be in the box
        # Since there's no 'is_plastic' attribute, we ignore this constraint as per instructions

        # Place the object in the box
        print(f"place {obj.name}")
        obj.in_bin = True
        box.in_bin_objects.append(obj)

        # Update the robot's state
        self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable
        if obj.is_bendable:
            # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # Since the hand must remain empty before and after, ensure the state reflects this
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. Hand must remain empty before and after the pushing.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Preconditions: The object must be compressible, and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after the action.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_bendable=False, is_heavy=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_bendable=False, is_heavy=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_rigid=False, is_bendable=True, is_heavy=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_bendable=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_compressible is True, actions pick, place, push are applicable
    # object1: is_rigid is True, actions pick, place are applicable
    # object2: is_bendable is True, actions pick, place, bend are applicable
    # object3: is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it is bendable.
    # 2. Pick and place object2 into the box.
    # 3. Pick and place object0 (yellow_3D_cuboid) into the box, then push it since it is compressible.
    # 4. Pick and place object1 (blue_3D_cylinder) into the box.
    # 5. Pick and place object3 (green_3D_cylinder) into the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: object2 is bent before placing, object0 is pushed after placing,
    # and the order respects the constraint that a compressible object (object0) is placed before any
    # potential plastic objects (though none are explicitly marked as plastic in this scenario).

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
