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
            # Effect: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint is applicable
        if hasattr(obj, 'material') and obj.material == 'plastic':
            # Check if there is a compressible object already in the box
            compressible_in_box = any(
                hasattr(o, 'material') and o.material == 'compressible' for o in box.in_bin_objects
            )
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Proceed to place the object
        print(f"place {obj.name}")
        self.state_handempty()  # Assuming the robot's hand becomes empty after placing the object
        box.in_bin_objects.append(obj)  # Add the object to the box's list of objects

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

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional attributes for demonstration purposes
    object0.is_compressible = True  # Example assumption
    object1.is_foldable = True      # Example assumption
    object2.is_bendable = True      # Example assumption
    object3.is_bendable = True      # Example assumption
    object4.is_compressible = True  # Example assumption

    # the object0.is_compressible is True, actions pick, place, push are applicable
    # the object1.is_foldable is True, actions pick, place, fold are applicable
    # the object2.is_bendable is True, actions pick, place, bend are applicable
    # the object3.is_bendable is True, actions pick, place, bend are applicable
    # the object4.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 and object3 before placing them.
    # 2. Fold object1 before placing it.
    # 3. Place object0 and object4, then push them after placing.
    # 4. Place all objects in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object2
    action.bend(object2, box)
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)

    # Bend object3
    action.bend(object3, box)
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Fold object1
    action.fold(object1, box)
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object0, then push
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    # Pick and place object4, then push
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by bending bendable objects before placing, folding foldable objects before placing,
    # and pushing compressible objects after placing. Non-plastic objects are placed without additional constraints.

    # Finally, add this code    
    print("All task planning is done")
