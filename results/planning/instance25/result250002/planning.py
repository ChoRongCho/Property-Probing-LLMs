from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # physical state of an object for {self.task}
    in_bin: bool

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
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is not empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            # If the constraint is satisfied or not applicable, proceed with placing
            if compressible_present:
                print(f"place {obj.name}")
                self.state_handempty()  # Assuming the robot is now empty-handed after placing
                box.in_bin_objects.append(obj)  # Update the box's state
            else:
                print(f"Cannot place {obj.name} - compressible object required first")
        else:
            # For non-plastic objects, place without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Assuming the robot is now empty-handed after placing
            box.in_bin_objects.append(obj)  # Update the box's state

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes
    object0.is_compressible = False
    object0.is_foldable = False
    object0.is_bendable = False
    object0.is_plastic = False

    object1.is_compressible = False
    object1.is_foldable = False
    object1.is_bendable = False
    object1.is_plastic = False

    object2.is_compressible = False
    object2.is_foldable = False
    object2.is_bendable = True
    object2.is_plastic = False

    object3.is_compressible = True
    object3.is_foldable = False
    object3.is_bendable = False
    object3.is_plastic = False

    # the object0.is_compressible is False, actions pick, place are applicable
    # the object1.is_compressible is False, actions pick, place are applicable
    # the object2.is_bendable is True, actions pick, place, bend are applicable
    # the object3.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: object2 (bend), object3 (push), object0, object1

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object2 before placing
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    # Pick and place object3, then push
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Object2 is bendable, so it is bent before placing. Object3 is compressible, so it is pushed after placing.
    # Objects 0 and 1 have no special constraints, so they are simply picked and placed.

    # Finally, add this code    
    print("All task planning is done")
