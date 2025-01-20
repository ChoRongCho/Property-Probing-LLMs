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
            # Effect: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is plastic and if the constraint is applicable
        if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
            # Check if a compressible object is already in the box
            compressible_in_box = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # If constraints are not applicable or satisfied, proceed with placing the object
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
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
object0 = Object(index=0, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0.is_foldable is True, actions pick, place, fold are applicable
    # object1.is_foldable is True, actions pick, place, fold are applicable
    # object2.is_bendable is True, actions pick, place, bend are applicable
    # object3.is_bendable is True, actions pick, place, bend are applicable
    # object4.is_compressible is True, actions pick, place, push are applicable
    # object5.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0, pick object0, place object0
    # 2. Fold object1, pick object1, place object1
    # 3. Bend object2, pick object2, place object2
    # 4. Bend object3, pick object3, place object3
    # 5. Pick object4, place object4, push object4
    # 6. Pick object5, place object5, push object5

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object0
    action.fold(object0, box)
    # Pick object0
    action.pick(object0, box)
    # Place object0
    action.place(object0, box)

    # Fold object1
    action.fold(object1, box)
    # Pick object1
    action.pick(object1, box)
    # Place object1
    action.place(object1, box)

    # Bend object2
    action.bend(object2, box)
    # Pick object2
    action.pick(object2, box)
    # Place object2
    action.place(object2, box)

    # Bend object3
    action.bend(object3, box)
    # Pick object3
    action.pick(object3, box)
    # Place object3
    action.place(object3, box)

    # Pick object4
    action.pick(object4, box)
    # Place object4
    action.place(object4, box)
    # Push object4
    action.push(object4, box)

    # Pick object5
    action.pick(object5, box)
    # Place object5
    action.place(object5, box)
    # Push object5
    action.push(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold before picking foldable objects, bend before picking bendable objects,
    # and push compressible objects after placing them in the box. The sequence ensures that all objects are placed
    # in the box following their respective constraints and the goal state is achieved.

    # Finally, add this code    
    print("All task planning is done")
