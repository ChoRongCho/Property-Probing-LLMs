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
    is_packable: bool


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
        # Preconditions: The robot's hand must be empty, the object must not be in the box, and the object must be packable.
        if self.robot_handempty and not obj.in_bin and obj.is_packable:
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
            box.in_bin_objects.append(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is currently holding the object and the object is packable
        if self.robot_now_holding == obj and obj.is_packable:
            # If the object is plastic, check if there is a compressible object already in the box
            if obj.is_plastic:
                compressible_in_box = any(o.is_bendable for o in box.in_bin_objects)
                if not compressible_in_box:
                    print(f"Cannot place {obj.name}")
                    return
            
            # Place the object in the box
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        if self.robot_handempty and obj.is_bendable and not obj.is_plastic:
            print(f"bend {obj.name}")
            # No change in state is needed as the hand remains empty before and after bending.
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_packable=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_packable=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=True, is_plastic=False, is_packable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_plastic=True, is_packable=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_plastic=False, is_packable=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0 is rigid and packable, actions pick, place are applicable
    # object1 is plastic and packable, actions pick, place are applicable
    # object2 is bendable and packable, actions pick, place, bend are applicable
    # object3 is plastic and packable, actions pick, place are applicable
    # object4 is rigid and packable, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it is bendable.
    # 2. Pick and place object2 (black_1D_line) into the box.
    # 3. Push object2 (black_1D_line) since it is compressible.
    # 4. Pick and place object0 (blue_3D_cylinder) into the box.
    # 5. Pick and place object4 (green_3D_cylinder) into the box.
    # 6. Pick and place object1 (blue_2D_rectangle) into the box (after object2 is in the box).
    # 7. Pick and place object3 (gray_1D_line) into the box (after object2 is in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)  # Bend the bendable object
    action.pick(object2, box)  # Pick the bendable object
    action.place(object2, box) # Place the bendable object
    action.push(object2, box)  # Push the compressible object

    action.pick(object0, box)  # Pick the rigid object
    action.place(object0, box) # Place the rigid object

    action.pick(object4, box)  # Pick the rigid object
    action.place(object4, box) # Place the rigid object

    action.pick(object1, box)  # Pick the plastic object
    action.place(object1, box) # Place the plastic object

    action.pick(object3, box)  # Pick the plastic object
    action.place(object3, box) # Place the plastic object

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing it, ensure a compressible object is in the box before placing plastic objects, and push compressible objects after placing them. Non-plastic objects are placed without constraints.

    # Finally, add this code    
    print("All task planning is done")
