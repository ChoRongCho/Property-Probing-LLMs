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
        # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            self.state_holding(obj)  # Effect: The robot is now holding the object.
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is of type 'plastic' and if the constraint applies
        if obj.object_type == 'plastic':
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == 'compressible' for o in box.in_bin_objects)
            if compressible_present:
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the box
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # For non-plastic objects, place without constraints
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            self.state_handempty()
            box.in_bin_objects.append(obj)

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
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes
    object0.is_rigid = True
    object1.is_compressible = True
    object2.is_foldable = True
    object3.is_bendable = True
    
    # the object0.is_rigid is True, actions pick, place are applicable
    # the object1.is_compressible is True, actions pick, place, push are applicable
    # the object2.is_foldable is True, actions pick, place, fold are applicable
    # the object3.is_bendable is True, actions pick, place, bend are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True 
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object2 (2D foldable) before picking and placing it.
    # 2. Pick and place object1 (3D compressible), then push it.
    # 3. Bend object3 (1D bendable) before picking and placing it.
    # 4. Pick and place object0 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object2
    action.fold(object2, box)
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)

    # Pick and place object1, then push
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    # Bend object3
    action.bend(object3, box)
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold before placing foldable objects, push compressible objects after placing,
    # and bend bendable objects before placing. The sequence ensures that all objects are placed in the box
    # according to their physical properties and constraints.

    # Finally, add this code    
    print("All task planning is done")
