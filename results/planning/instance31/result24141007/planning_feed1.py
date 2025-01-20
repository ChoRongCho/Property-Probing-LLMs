from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # physical state of an object for bin_packing
    in_bin: bool

    # Object physical properties
    is_rigid: bool
    is_bendable: bool
    is_plastic: bool

    # Additional predicates for bin_packing (max: 1)
    is_3D: bool


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
        # Preconditions: The object is not in the bin, the robot's hand is empty, and the object is rigid, bendable, or plastic with a compressible object in the box.
        if not obj.in_bin and self.robot_handempty and (obj.is_rigid or obj.is_bendable or (obj.is_plastic and any(o.is_bendable for o in box.in_bin_objects))):
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is plastic and if the constraint can be applied
        if obj.is_plastic:
            # Check if there is a compressible object already in the box
            compressible_present = any(o.is_bendable for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # Preconditions: The robot must be holding the object
        if self.robot_now_holding == obj:
            # Effect: Place the object in the box
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()  # Robot hand is now empty after placing the object
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def push(self, obj, box):
        # Check if the object is bendable (compressible) and in the box
        if obj.is_bendable and obj.in_bin:
            print(f"push {obj.name}")
        else:
            print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_3D=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=True, is_plastic=False, is_3D=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_3D=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True, actions pick, place are applicable
    # object1.is_plastic is True, actions pick, place are applicable (requires compressible object in box first)
    # object2.is_bendable is True, actions pick, place, push are applicable
    # object3.is_plastic is True, actions pick, place are applicable (requires compressible object in box first)
    # object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it is bendable.
    # 2. Pick and place object2 into the box.
    # 3. Push object2 in the box.
    # 4. Pick and place object0 (blue_3D_cylinder) into the box.
    # 5. Pick and place object4 (green_3D_cylinder) into the box.
    # 6. Pick and place object1 (blue_2D_rectangle) into the box (object2 is compressible).
    # 7. Pick and place object3 (gray_1D_line) into the box (object2 is compressible).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object2
    action.bend(object2, box)
    
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)
    
    # Push object2
    action.push(object2, box)
    
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)
    
    # Pick and place object4
    action.pick(object4, box)
    action.place(object4, box)
    
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)
    
    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bendable objects are bent before placing, plastic objects are placed only after a compressible object is in the box, and compressible objects are pushed after placing. The sequence ensures all objects reach their goal state of being packed in the box.

    # Finally, add this code    
    print("All task planning is done")

