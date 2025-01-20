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
        # Preconditions: The object must not be in the box, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # If constraints are not applicable or satisfied, place the object
        print(f"place {obj.name}")
        
        # Update the state to reflect the object being placed
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
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object5 = Object(index=5, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming we have additional properties for objects: is_foldable, is_compressible, is_bendable, is_plastic
    # Example properties (these should be defined based on the problem context):
    object0.is_compressible = False
    object0.is_foldable = False
    object0.is_bendable = False
    object0.is_plastic = False

    object1.is_compressible = False
    object1.is_foldable = True
    object1.is_bendable = False
    object1.is_plastic = False

    object2.is_compressible = False
    object2.is_foldable = True
    object2.is_bendable = False
    object2.is_plastic = False

    object3.is_compressible = False
    object3.is_foldable = False
    object3.is_bendable = False
    object3.is_plastic = False

    object4.is_compressible = True
    object4.is_foldable = False
    object4.is_bendable = False
    object4.is_plastic = False

    object5.is_compressible = False
    object5.is_foldable = False
    object5.is_bendable = False
    object5.is_plastic = False

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: object4 (compressible), object1 (foldable), object2 (foldable), object0, object3, object5

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Pick and place object4 (compressible)
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Fold, pick, and place object1 (foldable)
    action.fold(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    # Fold, pick, and place object2 (foldable)
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Pick and place object5
    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: compressible objects are pushed after placing, foldable objects are folded before picking and placing.
    # Non-plastic objects are placed without additional constraints. The sequence ensures all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
