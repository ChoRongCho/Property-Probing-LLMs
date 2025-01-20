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
        # Preconditions: The object is not in the box, and the robot's hand is empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is not empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is a plastic object and if the constraint is applicable
        if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
            # Check if there's a compressible object already in the box
            if any(o.object_type == "compressible" for o in box.in_bin_objects):
                print(f"place {obj.name}")
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # For non-plastic objects or if the constraint is not applicable
            print(f"place {obj.name}")
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
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0: is_rigid = True, actions pick, place are applicable
    # object1: is_rigid = True, actions pick, place are applicable
    # object2: is_foldable = True, actions pick, place, fold are applicable
    # object3: is_bendable = True, actions pick, place, bend are applicable
    # object4: is_compressible = True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: 
    # 1. Bend object3 (gray_1D_line) before placing.
    # 2. Pick and place object3.
    # 3. Pick and place object0 (yellow_3D_cuboid).
    # 4. Pick and place object1 (white_3D_cylinder).
    # 5. Fold object2 (transparent_2D_circle) before placing.
    # 6. Pick and place object2.
    # 7. Pick and place object4 (brown_3D_cylinder).
    # 8. Push object4 after placing.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)  # Bend object3
    action.pick(object3, box)  # Pick object3
    action.place(object3, box) # Place object3

    action.pick(object0, box)  # Pick object0
    action.place(object0, box) # Place object0

    action.pick(object1, box)  # Pick object1
    action.place(object1, box) # Place object1

    action.fold(object2, box)  # Fold object2
    action.pick(object2, box)  # Pick object2
    action.place(object2, box) # Place object2

    action.pick(object4, box)  # Pick object4
    action.place(object4, box) # Place object4
    action.push(object4, box)  # Push object4

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bending and folding actions are performed before picking and placing.
    # Compressible objects are pushed after being placed. Non-plastic objects are placed without constraints.
    # The sequence ensures all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
