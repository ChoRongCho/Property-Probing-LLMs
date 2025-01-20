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
        # Check if the object is plastic and if a compressible object is required in the box
        if obj.object_type == "plastic" and hasattr(obj, 'is_compressible'):
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        self.state_handempty()
        obj.in_bin = True
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
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, actions pick, place are applicable
    # object1: is_foldable is True, actions pick, place, fold are applicable
    # object2: is_bendable is True, actions pick, place, bend are applicable
    # object3: is_compressible is True, actions pick, place, push are applicable
    # object4: is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (if bendable), then pick and place it.
    # 2. Pick and place object3 (compressible), then push it.
    # 3. Fold object1 (if foldable), then pick and place it.
    # 4. Pick and place object0.
    # 5. Pick and place object4.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)  # Bend object2
    action.pick(object2, box)  # Pick object2
    action.place(object2, box) # Place object2

    action.pick(object3, box)  # Pick object3
    action.place(object3, box) # Place object3
    action.push(object3, box)  # Push object3

    action.fold(object1, box)  # Fold object1
    action.pick(object1, box)  # Pick object1
    action.place(object1, box) # Place object1

    action.pick(object0, box)  # Pick object0
    action.place(object0, box) # Place object0

    action.pick(object4, box)  # Pick object4
    action.place(object4, box) # Place object4

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are done before picking, 
    # and compressible objects are pushed after placing. Plastic objects are placed 
    # after a compressible object is already in the box. The sequence ensures all 
    # objects are placed in the box according to the goal states.

    # Finally, add this code    
    print("All task planning is done")
