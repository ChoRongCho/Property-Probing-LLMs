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
            # The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object.
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
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes
    object0.is_rigid = True  # Example: rigid objects can be picked and placed
    object1.is_compressible = True  # Example: compressible objects can be picked, placed, and pushed
    object2.is_foldable = True  # Example: foldable objects can be picked, placed, and folded
    object3.is_bendable = True  # Example: bendable objects can be picked, placed, and bent
    object4.is_rigid = True  # Example: rigid objects can be picked and placed

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (if bendable)
    # 2. Pick object3
    # 3. Place object3
    # 4. Pick object1 (compressible)
    # 5. Place object1
    # 6. Push object1
    # 7. Fold object2 (if foldable)
    # 8. Pick object2
    # 9. Place object2
    # 10. Pick object0
    # 11. Place object0
    # 12. Pick object4
    # 13. Place object4

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object3 if applicable
    if hasattr(object3, 'is_bendable') and object3.is_bendable:
        action.bend(object3, box)
    
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)
    
    # Pick, place, and push object1
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)
    
    # Fold object2 if applicable
    if hasattr(object2, 'is_foldable') and object2.is_foldable:
        action.fold(object2, box)
    
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)
    
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)
    
    # Pick and place object4
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before picking, 
    # compressible objects are pushed after placing, and plastic constraints are respected.

    # Finally, add this code    
    print("All task planning is done")
