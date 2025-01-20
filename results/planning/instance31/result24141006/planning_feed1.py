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

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The robot's hand must be empty, the object must not be in the box, and the object must be packable.
        if self.robot_handempty and not obj.in_bin and obj.is_packable:
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object and the object must be packable.
        if self.robot_now_holding == obj and obj.is_packable:
            # If the object is plastic, check if there is a compressible object already in the box
            if obj.is_plastic:
                compressible_in_box = any(o.is_bendable for o in box.in_bin_objects)
                if not compressible_in_box:
                    print(f"Cannot place {obj.name}")
                    return
            
            # Effects: Place the object in the box and the robot's hand becomes empty.
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be bendable and already in the box.
        if obj.is_bendable and obj.in_bin and not obj.is_plastic:
            print(f"push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")

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
    # object0: is_rigid=True, is_bendable=False, is_plastic=False, actions: pick, place
    # object1: is_rigid=False, is_bendable=False, is_plastic=True, actions: pick, place
    # object2: is_rigid=False, is_bendable=True, is_plastic=False, actions: pick, place, bend, push
    # object3: is_rigid=False, is_bendable=False, is_plastic=True, actions: pick, place
    # object4: is_rigid=True, is_bendable=False, is_plastic=False, actions: pick, place

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
    action.bend(object2, box)  # Bend object2
    action.pick(object2, box)  # Pick object2
    action.place(object2, box)  # Place object2
    action.push(object2, box)  # Push object2

    action.pick(object0, box)  # Pick object0
    action.place(object0, box)  # Place object0

    action.pick(object4, box)  # Pick object4
    action.place(object4, box)  # Place object4

    action.pick(object1, box)  # Pick object1
    action.place(object1, box)  # Place object1

    action.pick(object3, box)  # Pick object3
    action.place(object3, box)  # Place object3

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence ensures that all objects are packed according to their properties and constraints.
    # Object2 is bendable and must be bent before being placed. It is also compressible, so it is pushed after placement.
    # Object1 and object3 are plastic and require a compressible object (object2) to be in the box before they can be placed.
    # Non-plastic objects (object0 and object4) can be placed without additional constraints.

    # Finally, add this code    
    print("All task planning is done")

