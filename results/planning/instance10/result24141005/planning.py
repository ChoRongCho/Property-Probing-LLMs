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
    is_plastic: bool
    is_rigid: bool
    is_compressible: bool

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
        # Preconditions: The object is not in the bin and the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.

        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic and obj.is_compressible:
            # Check if there is already a compressible object in the box
            if any(o.is_compressible for o in box.in_bin_objects):
                print(f"place {obj.name}")
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name} - no compressible object in the box")
        else:
            # If the object is not plastic or the constraint does not apply, place it
            print(f"place {obj.name}")
            self.state_handempty()
            box.in_bin_objects.append(obj)

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            # Preconditions: The robot hand must be empty to push
            if self.robot_handempty:
                # Action Description: Push a 3D compressible object downward in the bin.
                print(f"push {obj.name}")
                # Effects: The robot hand remains empty after pushing
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name} because the hand is not empty")
        else:
            print(f"Cannot push {obj.name} due to constraints")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_compressible=False, is_3D=True)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_compressible=False, is_3D=True)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_compressible=False, is_3D=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=False, is_compressible=True, is_3D=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_compressible=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_plastic is True, actions pick, place are applicable (with constraints)
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_rigid is True, actions pick, place are applicable
    # the object3.is_compressible is True, actions pick, place, push are applicable
    # the object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object3 (compressible) into the box, then push it.
    # 2. Pick and place object1 (non-plastic) into the box.
    # 3. Pick and place object2 (non-plastic) into the box.
    # 4. Pick and place object4 (non-plastic) into the box.
    # 5. Pick and place object0 (plastic) into the box (after object3 is already in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object4, box)
    action.place(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: object3 is placed first as it is compressible, allowing object0 (plastic) to be placed later.
    # Non-plastic objects (object1, object2, object4) are placed without constraints.
    # The push action is applied to object3 after placing it in the box, as required.

    # Finally, add this code    
    print("All task planning is done")
