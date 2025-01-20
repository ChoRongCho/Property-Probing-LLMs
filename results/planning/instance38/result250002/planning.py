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
                self.state_handempty()  # Effect: Robot hand is now empty after placing the object
                box.in_bin_objects.append(obj)  # Effect: Object is now in the box
            else:
                print(f"Cannot place {obj.name}")
        else:
            # If the object is non-plastic or the constraint is not applicable, place it without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Effect: Robot hand is now empty after placing the object
            box.in_bin_objects.append(obj)  # Effect: Object is now in the box

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0.is_foldable = True
    # object1.is_bendable = True
    # object2.is_compressible = True
    # object3.is_rigid = True

    # the object0.is_foldable is True, actions pick, place, fold are applicable
    # the object1.is_bendable is True, actions pick, place, bend are applicable
    # the object2.is_compressible is True, actions pick, place, push are applicable
    # the object3.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o)
    # !!Note2: Do not assume or change the physical properties of the object.
    # Write here.
    # 1. Fold object0 (if foldable), then pick and place it.
    # 2. Bend object1 (if bendable), then pick and place it.
    # 3. Pick and place object2, then push it (if compressible).
    # 4. Pick and place object3.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object0 if foldable
    if hasattr(object0, 'is_foldable') and object0.is_foldable:
        action.fold(object0, box)
    
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Bend object1 if bendable
    if hasattr(object1, 'is_bendable') and object1.is_bendable:
        action.bend(object1, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)

    # Push object2 if compressible
    if hasattr(object2, 'is_compressible') and object2.is_compressible:
        action.push(object2, box)

    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by ensuring foldable and bendable objects are processed before picking.
    # Compressible objects are pushed after being placed. The sequence respects the constraints for plastic objects.

    # Finally, add this code    
    print("All task planning is done")
