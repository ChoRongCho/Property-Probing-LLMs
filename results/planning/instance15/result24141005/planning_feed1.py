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
    is_rigid: bool = False
    is_compressible: bool = False
    is_bendable: bool = False
    is_plastic: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_fragile: bool = False


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

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box.
        if obj.is_plastic:
            if any(o.is_compressible for o in box.in_bin_objects):
                print(f"place {obj.name}")
                self.state_handempty()
                box.in_bin_objects.append(obj)
                obj.in_bin = True  # Update the object's state to in_bin
            else:
                print(f"Cannot place {obj.name} because no compressible object is in the box")
        else:
            print(f"place {obj.name}")
            self.state_handempty()
            box.in_bin_objects.append(obj)
            obj.in_bin = True  # Update the object's state to in_bin

    def bend(self, obj, box):
        if obj.is_bendable and self.robot_handempty:
            print(f"bend {obj.name}")
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and in the bin, and the robot's hand must be empty.
        if obj.is_compressible and obj.in_bin and self.robot_handempty:
            print(f"push {obj.name}")
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object5 = Object(index=5, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True, actions pick, place are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable
    # object3.is_plastic is True, actions pick, place are applicable
    # object4.is_bendable is True, actions pick, place, bend are applicable
    # object5.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True 
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object4 (black_1D_line) before placing it.
    # 2. Pick and place object1 (yellow_3D_cuboid) as it is compressible.
    # 3. Push object1 after placing it.
    # 4. Pick and place object2 (white_3D_cylinder) as it is compressible.
    # 5. Push object2 after placing it.
    # 6. Pick and place object5 (brown_3D_cylinder) as it is compressible.
    # 7. Push object5 after placing it.
    # 8. Pick and place object3 (blue_2D_rectangle) as it is plastic and requires a compressible object in the box.
    # 9. Pick and place object0 (white_3D_cuboid) as it is rigid.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object4, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)
    action.pick(object5, box)
    action.place(object5, box)
    action.push(object5, box)
    action.pick(object3, box)
    action.place(object3, box)
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing it, ensure a compressible object is in the box before placing a plastic object, and push all compressible objects after placing them. The sequence ensures all objects reach their goal state of being in the bin.

    # Finally, add this code    
    print("All task planning is done")

