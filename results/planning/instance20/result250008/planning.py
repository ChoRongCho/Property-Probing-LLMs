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
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if not compressible_in_box:
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
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes
    object0.is_rigid = True
    object1.is_rigid = True
    object2.is_bendable = True
    object3.is_compressible = True
    object4.is_rigid = True

    # the object0.is_rigid is True, actions pick, place are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_bendable is True, actions pick, place, bend are applicable
    # the object3.is_compressible is True, actions pick, place, push are applicable
    # the object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (bendable) before placing.
    # 2. Pick and place object3 (compressible), then push it.
    # 3. Pick and place object0, object1, and object4 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object2
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    # Pick, place, and push object3
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object4
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Object2 is bendable, so it was bent before placing. Object3 is compressible, so it was pushed after placing.
    # Objects 0, 1, and 4 are rigid and were placed without additional actions.
    # The sequence respects the constraints for plastic and compressible objects.

    # Finally, add this code    
    print("All task planning is done")
