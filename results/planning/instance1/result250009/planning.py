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
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint is applicable
        if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
            # Check if there is a compressible object already in the box
            if any(o.object_type == "compressible" for o in box.in_bin_objects):
                print(f"place {obj.name}")
                self.state_handempty()  # Assuming the robot places the object and becomes handempty
                box.in_bin_objects.append(obj)  # Update the box's state
            else:
                print(f"Cannot place {obj.name}")
        else:
            # If the object is non-plastic or the constraint is not applicable, place it without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Assuming the robot places the object and becomes handempty
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
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False)
object2 = Object(index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0 is a 3D object, actions pick, place are applicable
    # the object1 is a 3D object, actions pick, place are applicable
    # the object2 is a 3D object, actions pick, place are applicable
    # Note: No additional properties like compressible, foldable, or bendable are provided.

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True 
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Since no specific properties like compressible, foldable, or bendable are given, we assume all objects are non-plastic and can be placed directly.
    # Order: pick -> place for each object

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Since no objects have properties like compressible, foldable, or bendable, the actions are straightforward.
    # All objects are picked and placed directly into the box without additional actions like bending, folding, or pushing.
    # The goal state is achieved as all objects are now in the box.

    # Finally, add this code    
    print("All task planning is done")
