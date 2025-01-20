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
            # Effect: The robot is now holding the object, and the object is considered in the box.
            self.state_holding(obj)
            obj.in_bin = True
            box.in_bin_objects.append(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return

        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state to hand empty
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object2 = Object(index=2, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assume we have additional properties for objects: is_compressible, is_bendable, is_foldable, is_plastic
    # For demonstration, let's assume:
    # object0: is_rigid=True, actions pick, place are applicable
    # object1: is_rigid=True, actions pick, place are applicable
    # object2: is_compressible=True, actions pick, place, push are applicable
    # object3: is_foldable=True, actions pick, place, fold are applicable
    # object4: is_bendable=True, actions pick, place, bend are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (if foldable), then pick and place it.
    # 2. Bend object4 (if bendable), then pick and place it.
    # 3. Pick and place object2, then push it (if compressible).
    # 4. Pick and place object0.
    # 5. Pick and place object1.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object3 if foldable
    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    # Bend object4 if bendable
    action.bend(object4, box)
    action.pick(object4, box)
    action.place(object4, box)

    # Pick and place object2, then push it if compressible
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before picking and placing.
    # Compressible objects are pushed after being placed. Non-plastic objects are placed without constraints.
    # The sequence ensures all objects are placed in the box, achieving the goal states.

    # Finally, add this code    
    print("All task planning is done")
