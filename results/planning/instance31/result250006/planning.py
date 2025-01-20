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
        # Action Description: Pick an object that is not in the box. 
        # The action does not include the 'place' action and can be applied to any type of object.
        
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the object is considered in the robot's possession.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is a plastic object and if a compressible object is already in the box
        if obj.object_type == "plastic":
            compressible_in_box = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if compressible_in_box or 'compressible' not in obj.__annotations__:
                print(f"place {obj.name}")
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
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
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assume additional properties for demonstration purposes:
    # object0.is_compressible = True
    # object1.is_foldable = True
    # object2.is_bendable = True
    # object3.is_bendable = True
    # object4.is_plastic = True

    # the object0.is_compressible is True, actions pick, place, push are applicable
    # the object1.is_foldable is True, actions pick, place, fold are applicable
    # the object2.is_bendable is True, actions pick, place, bend are applicable
    # the object3.is_bendable is True, actions pick, place, bend are applicable
    # the object4.is_plastic is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object0 (compressible), then push it.
    # 2. Fold object1 (foldable), pick and place it.
    # 3. Bend object2 (bendable), pick and place it.
    # 4. Bend object3 (bendable), pick and place it.
    # 5. Pick and place object4 (plastic) after a compressible object is in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.fold(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.bend(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by ensuring that compressible objects are pushed after placement,
    # foldable objects are folded before picking and placing, and bendable objects are bent before picking and placing.
    # The plastic object is placed after a compressible object is already in the box, adhering to the constraints.

    # Finally, add this code    
    print("All task planning is done")
