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
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is not empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check preconditions
        if not self.robot_handempty and not obj.in_bin:
            # Check if the object is plastic and if the constraint applies
            if obj.is_plastic:
                # Check if there is at least one non-plastic object in the box
                if any(not o.is_plastic for o in box.in_bin_objects):
                    print(f"place {obj.name}")
                    # Update the state to reflect the object is now in the bin
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} - no non-plastic object in the box")
            else:
                # For non-plastic objects, place without constraints
                print(f"place {obj.name}")
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name} - robot is not holding the object or object is already in bin")

    def push(self, obj, box):
        # Action Description: Push a compressible object. Hand must remain empty before and after the pushing action.
        # Assuming compressible objects are defined by a specific property, which is not currently defined.
        if self.robot_handempty and not obj.is_plastic:  # Assuming non-plastic objects can be compressible
            print(f"push {obj.name}")
            # Assuming the action does not change the state of the robot's hand
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, is_3D is True, actions pick, place, push are applicable
    # object1: is_plastic is True, actions pick, place are applicable
    # object2: is_bendable is True, actions pick, place, bend are applicable
    # object3: is_plastic is True, actions pick, place are applicable
    # object4: is_rigid is True, is_3D is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it is bendable.
    # 2. Pick and place object2 into the box.
    # 3. Push object0 (blue_3D_cylinder) since it is compressible.
    # 4. Pick and place object0 into the box.
    # 5. Pick and place object1 (blue_2D_rectangle) into the box.
    # 6. Pick and place object3 (gray_1D_line) into the box.
    # 7. Push object4 (green_3D_cylinder) since it is compressible.
    # 8. Pick and place object4 into the box.

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

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bendable objects are bent before placing, compressible objects are pushed after placing, and plastic objects are placed only after a compressible object is in the box. The sequence ensures all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
