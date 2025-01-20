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
    is_plastic: bool

    # Additional predicates for bin_packing (max: 1)
    is_packable: bool


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
        # Preconditions: The object must not be in the bin, the robot hand must be empty, and the object must be packable.
        if not obj.in_bin and self.robot_handempty and obj.is_packable:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the robot is holding the object and the object is packable
        if self.robot_now_holding == obj and obj.is_packable:
            # Check if the object is plastic and ensure a compressible object is already in the box
            if obj.is_plastic:
                if any(o.is_compressible for o in box.in_bin_objects):
                    print(f"place {obj.name}")
                    self.state_handempty()
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                else:
                    print(f"Cannot place {obj.name} - requires a compressible object in the box first")
            else:
                # For non-plastic objects, place without constraints
                print(f"place {obj.name}")
                self.state_handempty()
                obj.in_bin = True
                box.in_bin_objects.append(obj)
        else:
            print(f"Cannot place {obj.name} - not holding or not packable")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.is_compressible and obj.in_bin:
            print(f"push {obj.name}")
            # Since the hand must remain empty before and after, no state change is needed.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_plastic=False, is_packable=False)
object2 = Object(index=2, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_plastic=True, is_packable=False)
object4 = Object(index=4, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False
    # object1: is_rigid=False, is_compressible=True, is_plastic=False, is_packable=False
    # object2: is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False
    # object3: is_rigid=False, is_compressible=False, is_plastic=True, is_packable=False
    # object4: is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object1 (compressible), then push it.
    # 2. Pick and place object3 (plastic) after object1 is in the box.
    # 3. Pick and place object0, object2, and object4 (non-plastic) without constraints.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Attempt to pick and place each object according to the rules
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: object1 is placed first as it is compressible and pushed afterward.
    # Object3 is plastic and placed after object1 is in the box. Non-plastic objects (object0, object2, object4) are placed without constraints.
    # The sequence respects the constraints of not bending, folding, or pushing plastic objects.

    # Finally, add this code    
    print("All task planning is done")
