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
        # Preconditions: The object is not in the box and the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is a plastic object and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            # If a compressible object is present, or if the constraint does not apply, proceed
            if compressible_present:
                print(f"place {obj.name}")
                self.state_handempty()  # Update the robot's state to hand empty
                box.in_bin_objects.append(obj)  # Add the object to the box
            else:
                print(f"Cannot place {obj.name}")
        else:
            # For non-plastic objects, place without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Update the robot's state to hand empty
            box.in_bin_objects.append(obj)  # Add the object to the box

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
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming the physical properties of objects are defined elsewhere, let's define them here for clarity:
    # object0: is_rigid = True, is_compressible = False, is_foldable = False, is_bendable = False
    # object1: is_rigid = True, is_compressible = False, is_foldable = False, is_bendable = False
    # object2: is_rigid = False, is_compressible = False, is_foldable = True, is_bendable = False
    # object3: is_rigid = False, is_compressible = False, is_foldable = False, is_bendable = True
    # object4: is_rigid = True, is_compressible = True, is_foldable = False, is_bendable = False
    # object5: is_rigid = True, is_compressible = False, is_foldable = False, is_bendable = False

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: 
    # 1. Fold object2 (if foldable), then pick and place it.
    # 2. Bend object3 (if bendable), then pick and place it.
    # 3. Pick and place object4 (compressible), then push it.
    # 4. Pick and place object0, object1, and object5 (all rigid and non-plastic).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object2
    action.fold(object2, box)
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)

    # Bend object3
    action.bend(object3, box)
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Pick and place object4, then push
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object5
    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before picking, compressible objects are pushed after placing, and non-plastic objects are placed without constraints.

    # Finally, add this code    
    print("All task planning is done")
