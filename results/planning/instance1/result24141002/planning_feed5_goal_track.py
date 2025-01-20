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

    # Additional predicates for bin_packing (max: 1)
    is_heavy: bool = False


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

# only write a code here without example instantiation
# Note! If a predicate required by the constraints is not defined in the class Object, ignore the constraints!!!

# only write a code here without example instantiation
# Note! If a predicate required by the constraints is not defined in the class Object, ignore the constraints!!!

# only write a code here without example instantiation
# Note! If a predicate required by the constraints is not defined in the class Object, ignore the constraints!!!

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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic:
            # Check if there is a compressible object already in the box
            compressible_present = any(not o.is_rigid for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # If constraints are satisfied or not applicable, place the object
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state to hand empty
        self.state_handempty()

        # Push the object if it is compressible
        if not obj.is_rigid and not obj.is_plastic:
            self.push(obj, box)

    def push(self, obj, box):
        # Check if the object is compressible (not rigid) and not plastic
        if not obj.is_rigid and not obj.is_plastic:
            print(f"push {obj.name}")
        else:
            print('Cannot push')

    def bend(self, obj, box):
        print('Cannot bend')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_heavy=False)
object1 = Object(index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False)
object2 = Object(index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_plastic is True, object0.is_rigid is False, actions pick, place are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # According to the rules:
    # 1. Place a compressible object first if you want to place a plastic object.
    # 2. Push all compressible objects after placing them.
    # 3. No bendable or foldable objects are present, so no bending or folding actions are needed.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Pick and place the white_3D_cuboid (object1) first since it is rigid and has no constraints
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place the green_3D_cylinder (object2) next since it is also rigid and has no constraints
    action.pick(object2, box)
    action.place(object2, box)

    # Now, pick and place the red_3D_cuboid (object0), which is plastic
    # Since there are already objects in the box, the constraint is satisfied
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence ensures that the plastic object (red_3D_cuboid) is placed after a non-plastic object (white_3D_cuboid or green_3D_cylinder) is already in the box.
    # This satisfies the constraint that a compressible object should be in the box before placing a plastic object.
    # No bending or folding actions are needed as there are no bendable or foldable objects.
    # The push action is not applicable since the objects are either rigid or plastic.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
