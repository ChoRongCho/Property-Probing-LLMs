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
        # Preconditions: The object is not in the box, and the robot's hand is empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. 
            # The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic and obj.is_compressible:
            # Check if there is at least one compressible object already in the box
            if any(o.is_compressible for o in box.in_bin_objects):
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the box
                self.state_handempty()
                obj.in_bin = True
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name} - no compressible object in the box")
        else:
            # If the object is not plastic or the constraint does not apply, place it
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            self.state_handempty()
            obj.in_bin = True
            box.in_bin_objects.append(obj)

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            print(f"push {obj.name}")
            # Ensure the robot's hand is empty before and after the push
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_fragile=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_fragile=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_plastic=False, is_fragile=False)
object3 = Object(index=3, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_fragile=False)
object4 = Object(index=4, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_plastic=True, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_rigid is True, actions pick, place are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_compressible is True, actions pick, place, push are applicable
    # the object3.is_rigid is True, actions pick, place are applicable
    # the object4.is_plastic is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object2 (compressible), then push it.
    # 2. Pick and place object0.
    # 3. Pick and place object1.
    # 4. Pick and place object3.
    # 5. Pick and place object4 (plastic), ensuring object2 is already in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts with placing the compressible object (object2) and pushing it, 
    # ensuring that the rule for plastic objects is satisfied later. 
    # Non-plastic objects (object0, object1, object3) are placed without constraints.
    # Finally, the plastic object (object4) is placed after a compressible object is already in the box.

    # Finally, add this code    
    print("All task planning is done")
