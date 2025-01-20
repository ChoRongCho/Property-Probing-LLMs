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
        # Preconditions: The object is not in the box, and the robot's hand is empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint should be considered
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if compressible_present:
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the box
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # For non-plastic objects, place without constraints
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
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object5 = Object(index=5, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False)
object6 = Object(index=6, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming some hypothetical properties for demonstration purposes:
    # object0 is rigid, actions pick, place are applicable
    # object1 is compressible, actions pick, place, push are applicable
    # object2 is rigid, actions pick, place are applicable
    # object3 is foldable, actions pick, place, fold are applicable
    # object4 is foldable, actions pick, place, fold are applicable
    # object5 is bendable, actions pick, place, bend are applicable
    # object6 is compressible, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True 
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True
    # object6: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object5 (bendable) before placing.
    # 2. Pick and place object5.
    # 3. Pick and place object1 (compressible), then push.
    # 4. Pick and place object6 (compressible), then push.
    # 5. Fold object3 (foldable) before placing.
    # 6. Pick and place object3.
    # 7. Fold object4 (foldable) before placing.
    # 8. Pick and place object4.
    # 9. Pick and place object0 (rigid).
    # 10. Pick and place object2 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object5, box)
    action.pick(object5, box)
    action.place(object5, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object6, box)
    action.place(object6, box)
    action.push(object6, box)

    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.fold(object4, box)
    action.pick(object4, box)
    action.place(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before picking and placing.
    # Compressible objects are pushed after being placed. The sequence ensures all objects are placed
    # in the box according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")
