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
    is_bendable: bool = False
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
        # Preconditions: The object must not be in a bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic:
            # Check if there is at least one compressible object already in the box
            if any(o.is_compressible for o in box.in_bin_objects):
                print(f"place {obj.name}")
                # Effect: Update the state to reflect the object is now in the bin
                self.state_handempty()
                obj.in_bin = True
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # Non-plastic objects can be placed without constraints
            print(f"place {obj.name}")
            # Effect: Update the state to reflect the object is now in the bin
            self.state_handempty()
            obj.in_bin = True
            box.in_bin_objects.append(obj)

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Note: If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and obj.is_bendable and not obj.is_plastic:
            print(f"bend {obj.name}")
            # Effects: The robot's hand remains empty after bending.
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin.
        # Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.is_compressible and obj.is_3D:
            print(f"push {obj.name}")
            # No change in state as hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object5 = Object(index=5, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True, actions pick, place are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable
    # object3.is_plastic is True, actions pick, place are applicable (with constraints)
    # object4.is_bendable is True, actions bend, pick, place are applicable
    # object5.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object4 (black_1D_line) before placing it.
    # 2. Pick and place object1 (yellow_3D_cuboid) and push it after placing.
    # 3. Pick and place object2 (white_3D_cylinder) and push it after placing.
    # 4. Pick and place object5 (brown_3D_cylinder) and push it after placing.
    # 5. Pick and place object3 (blue_2D_rectangle) after a compressible object is in the box.
    # 6. Pick and place object0 (white_3D_cuboid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object4, box)  # Bend black_1D_line
    action.pick(object4, box)
    action.place(object4, box)

    action.pick(object1, box)  # Pick yellow_3D_cuboid
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object2, box)  # Pick white_3D_cylinder
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object5, box)  # Pick brown_3D_cylinder
    action.place(object5, box)
    action.push(object5, box)

    action.pick(object3, box)  # Pick blue_2D_rectangle
    action.place(object3, box)

    action.pick(object0, box)  # Pick white_3D_cuboid
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing, ensure a compressible object is in the box before placing a plastic object, and push all compressible objects after placing them. The sequence respects the constraints and ensures all objects reach their goal state of being in the bin.

    # Finally, add this code    
    print("All task planning is done")
