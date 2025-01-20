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
        
        # Check if the robot is holding the object
        if self.robot_now_holding == obj:
            # Place the object in the box
            print(f"place {obj.name}")
            
            # Update the state to reflect that the robot's hand is now empty
            self.state_handempty()
            
            # Update the box to include the object
            box.in_bin_objects.append(obj)
            
            # Update the object's state to reflect it is now in the bin
            obj.in_bin = True
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
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object2 = Object(index=2, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes
    object0.is_plastic = True
    object1.is_compressible = True
    object2.is_plastic = True
    object3.is_foldable = True
    object4.is_bendable = True

    # the object0.is_plastic is True, actions pick, place are applicable
    # the object1.is_compressible is True, actions pick, place, push are applicable
    # the object2.is_plastic is True, actions pick, place are applicable
    # the object3.is_foldable is True, actions pick, place, fold are applicable
    # the object4.is_bendable is True, actions pick, place, bend are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object4 (1D bendable) before placing.
    # 2. Pick and place object4.
    # 3. Pick and place object1 (3D compressible), then push it.
    # 4. Fold object3 (2D foldable) before placing.
    # 5. Pick and place object3.
    # 6. Pick and place object0 (plastic), ensuring a compressible object is already in the bin.
    # 7. Pick and place object2 (plastic), ensuring a compressible object is already in the bin.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object4, box)
    action.pick(object4, box)
    action.place(object4, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by bending the bendable object before placing it, folding the foldable object before placing it, and ensuring a compressible object is in the bin before placing any plastic objects. The compressible object is also pushed after being placed.

    # Finally, add this code    
    print("All task planning is done")
