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
            # Effect: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            if compressible_in_box:
                print(f"place {obj.name}")
                # Update the state to reflect the object is placed
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # If the object is non-plastic or the constraint does not apply, place it
            print(f"place {obj.name}")
            # Update the state to reflect the object is placed
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
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0.is_rigid = True, actions pick, place are applicable
    # object1.is_compressible = True, actions pick, place, push are applicable
    # object2.is_rigid = True, actions pick, place are applicable
    # object3.is_bendable = True, actions pick, place, bend are applicable
    # object4.is_rigid = True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (if bendable) before placing it.
    # 2. Pick and place object3.
    # 3. Pick and place object1, then push it (if compressible).
    # 4. Pick and place object0.
    # 5. Pick and place object2.
    # 6. Pick and place object4.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object3 if bendable
    action.bend(object3, box)
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)
    
    # Pick and place object1, then push it if compressible
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)
    
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)
    
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)
    
    # Pick and place object4
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by ensuring that bendable objects are bent before placing,
    # compressible objects are pushed after placing, and no unnecessary actions are performed on rigid objects.
    # The sequence ensures all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
