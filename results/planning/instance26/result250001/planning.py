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
        # Preconditions: The object must not be in the box, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is of type 'plastic' and the constraint applies
        if obj.object_type == 'plastic':
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == 'compressible' for o in box.in_bin_objects)
            
            # If the constraint is satisfied or not applicable, proceed with placing
            if compressible_present:
                print(f"place {obj.name}")
                self.state_handempty()  # Update the robot's state to hand empty after placing
                box.in_bin_objects.append(obj)  # Add the object to the box's list
            else:
                print(f"Cannot place {obj.name}")
        else:
            # For non-plastic objects, place without constraints
            print(f"place {obj.name}")
            self.state_handempty()  # Update the robot's state to hand empty after placing
            box.in_bin_objects.append(obj)  # Add the object to the box's list

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
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)

box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, actions pick, place are applicable
    # object1: is_rigid is True, actions pick, place are applicable
    # object2: is_foldable is True, actions pick, place, fold are applicable
    # object3: is_bendable is True, actions pick, place, bend are applicable
    # object4: is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume or change the physical properties of the object.
    # Write here.
    # 1. Bend object3 (gray_1D_line) since it is bendable.
    # 2. Pick and place object3 (gray_1D_line).
    # 3. Pick and place object4 (brown_3D_cylinder), then push it since it is compressible.
    # 4. Fold object2 (transparent_2D_circle) since it is foldable.
    # 5. Pick and place object2 (transparent_2D_circle).
    # 6. Pick and place object0 (yellow_3D_cuboid).
    # 7. Pick and place object1 (white_3D_cylinder).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)  # Bend the bendable object
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)  # Push the compressible object

    action.fold(object2, box)  # Fold the foldable object
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence of actions respects the constraints: bend and fold actions are performed before picking,
    # and compressible objects are pushed after placing. Non-plastic objects are placed without constraints,
    # and the sequence ensures all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
