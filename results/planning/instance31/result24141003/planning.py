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
    is_plastic: bool
    
    # Additional predicates for bin_packing (max: 1)
    is_3D: bool


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
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the robot is currently holding the object and the object is not already in the bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Check if the object is plastic and if the constraint can be ignored
            if obj.is_plastic:
                # Since the constraint about compressible objects is not applicable (no such property in Object class),
                # we ignore it and proceed with placing the object.
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the bin
                obj.in_bin = True
                # Update the robot's state to hand empty
                self.state_handempty()
            else:
                # For non-plastic objects, place without constraints
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the bin
                obj.in_bin = True
                # Update the robot's state to hand empty
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and obj.is_bendable and not obj.is_plastic:
            print(f"bend {obj.name}")
            # Assuming the effect is that the object is now in a bent state and ready to be placed in the box
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_3D=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=True, is_plastic=False, is_3D=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_3D=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, actions pick, place are applicable
    # object1: is_plastic is True, actions pick, place are applicable (requires a compressible object in the box first)
    # object2: is_bendable is True, actions pick, bend, place are applicable
    # object3: is_plastic is True, actions pick, place are applicable (requires a compressible object in the box first)
    # object4: is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it is bendable.
    # 2. Pick and place object2 into the box.
    # 3. Pick and place object0 (blue_3D_cylinder) since it is non-plastic.
    # 4. Pick and place object4 (green_3D_cylinder) since it is non-plastic.
    # 5. Pick and place object1 (blue_2D_rectangle) since a compressible object (object2) is already in the box.
    # 6. Pick and place object3 (gray_1D_line) since a compressible object (object2) is already in the box.

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
    action.pick(object4, box)
    action.place(object4, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts by bending the bendable object (object2) as required. This object is then placed in the box first,
    # allowing subsequent placement of plastic objects (object1 and object3) since a compressible object is now in the box.
    # Non-plastic objects (object0 and object4) are placed without constraints. The sequence respects all rules, ensuring
    # that plastic objects are placed only after a compressible object is in the box.

    # Finally, add this code    
    print("All task planning is done")
