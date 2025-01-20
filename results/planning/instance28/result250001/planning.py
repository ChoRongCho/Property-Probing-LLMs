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
        # Preconditions: The robot's hand must be empty, and the object must not already be in the box.
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Preconditions: The robot must be holding the object and the object should not already be in a bin.
        if self.robot_now_holding == obj and not obj.in_bin:
            print(f"place {obj.name}")
            # Effects: The object is placed in the bin, and the robot's hand is now empty.
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

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
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assume we have additional attributes for objects to define their properties.
    object0.is_plastic = False
    object0.is_compressible = False
    object0.is_bendable = False
    object0.is_foldable = False

    object1.is_plastic = False
    object1.is_compressible = False
    object1.is_bendable = False
    object1.is_foldable = True

    object2.is_plastic = False
    object2.is_compressible = False
    object2.is_bendable = True
    object2.is_foldable = False

    object3.is_plastic = False
    object3.is_compressible = True
    object3.is_bendable = False
    object3.is_foldable = False

    object4.is_plastic = True
    object4.is_compressible = False
    object4.is_bendable = False
    object4.is_foldable = False

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: object3 (compressible), object1 (foldable), object2 (bendable), object4 (plastic), object0 (rigid)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Place compressible object first
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    # Fold foldable object before placing
    action.fold(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    # Bend bendable object before placing
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    # Place plastic object after a compressible object is in the box
    action.pick(object4, box)
    action.place(object4, box)

    # Place remaining rigid object
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence ensures that all constraints are respected: compressible objects are pushed, foldable objects are folded, and bendable objects are bent before placing. Plastic objects are placed after a compressible object is in the box.

    # Finally, add this code    
    print("All task planning is done")
