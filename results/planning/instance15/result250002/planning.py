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
        # Check if the object is plastic and the constraint applies
        if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
            # Check if there is a compressible object already in the box
            compressible_in_box = any(
                hasattr(o, 'compressible') and o.compressible for o in box.in_bin_objects
            )
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
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object5 = Object(index=5, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional attributes for objects based on the rules:
    object0.is_rigid = True
    object1.is_rigid = True
    object2.is_compressible = True
    object3.is_foldable = True
    object4.is_bendable = True
    object5.is_compressible = True

    # the object0.is_rigid is True, actions pick, place are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_compressible is True, actions pick, place, push are applicable
    # the object3.is_foldable is True, actions pick, place, fold are applicable
    # the object4.is_bendable is True, actions pick, place, bend are applicable
    # the object5.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: 
    # 1. Bend object4 (if bendable)
    # 2. Pick and place object4
    # 3. Fold object3 (if foldable)
    # 4. Pick and place object3
    # 5. Pick and place object0
    # 6. Pick and place object1
    # 7. Pick, place, and push object2
    # 8. Pick, place, and push object5

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object4, box)
    action.pick(object4, box)
    action.place(object4, box)

    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object5, box)
    action.place(object5, box)
    action.push(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by bending and folding objects before placing them.
    # Compressible objects are pushed after being placed in the box.
    # Non-plastic objects are placed without additional constraints.
    # The sequence ensures that all objects reach their goal state of being in the box.

    # Finally, add this code    
    print("All task planning is done")
