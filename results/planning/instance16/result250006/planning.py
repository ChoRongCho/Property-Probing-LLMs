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
        # Preconditions: The robot's hand must be empty, and the object must not already be in the box.
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Preconditions: The robot must be holding the object, and the box must be available.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the robot is currently holding the object
        if self.robot_now_holding == obj:
            # Check if the object is plastic and if the constraint can be ignored
            if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
                # Check if a compressible object is already in the box
                if any(o.object_type == "compressible" for o in box.in_bin_objects):
                    print(f"place {obj.name}")
                    # Effect: The object is placed in the box, and the robot's hand is now empty
                    box.in_bin_objects.append(obj)
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} - no compressible object in the box")
            else:
                # If the object is not plastic or the constraint is ignored, place it without constraints
                print(f"place {obj.name}")
                # Effect: The object is placed in the box, and the robot's hand is now empty
                box.in_bin_objects.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name} - robot is not holding the object")

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
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0.is_rigid = True, actions pick, place are applicable
    # object1.is_rigid = True, actions pick, place are applicable
    # object2.is_compressible = True, actions pick, place, push are applicable
    # object3.is_foldable = True, actions pick, place, fold are applicable
    # object4.is_compressible = True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (foldable) before picking and placing it.
    # 2. Pick and place object2 (compressible) and push it after placing.
    # 3. Pick and place object4 (compressible) and push it after placing.
    # 4. Pick and place object0 (rigid).
    # 5. Pick and place object1 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object3
    action.fold(object3, box)
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)
    
    # Pick, place, and push object2
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)
    
    # Pick, place, and push object4
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)
    
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)
    
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, push compressible objects after placing,
    # and place rigid objects without additional constraints. The sequence ensures all objects are in the box as per the goal state.

    # Finally, add this code    
    print("All task planning is done")
