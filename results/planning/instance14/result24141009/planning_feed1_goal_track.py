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
    is_compressible: bool
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
        # Preconditions: The object must not be in the bin, and the robot hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object.
        if self.robot_now_holding == obj:
            # Check if the object is plastic and ensure a compressible object is already in the box
            if obj.is_plastic:
                if any(o.is_compressible for o in box.in_bin_objects):
                    print(f"place {obj.name}")
                    self.state_handempty()
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                else:
                    print(f"Cannot place {obj.name} - requires a compressible object in the box first")
            else:
                # For non-plastic objects, place without constraints
                print(f"place {obj.name}")
                self.state_handempty()
                obj.in_bin = True
                box.in_bin_objects.append(obj)
        else:
            print(f"Cannot place {obj.name} - not holding")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        if self.robot_handempty and obj.is_compressible and obj.in_bin:
            print(f"push {obj.name}")
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_plastic=False, is_packable=False)
object2 = Object(index=2, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_plastic=True, is_packable=False)
object4 = Object(index=4, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_packable=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True, actions pick, place are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_rigid is True, actions pick, place are applicable
    # object3.is_plastic is True, actions pick, place are applicable
    # object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object1 (compressible) and then push it.
    # 2. Pick and place object0 (non-plastic, no constraints).
    # 3. Pick and place object2 (non-plastic, no constraints).
    # 4. Pick and place object3 (plastic, requires compressible object already in the box).
    # 5. Pick and place object4 (non-plastic, no constraints).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts with placing the compressible object (object1) and pushing it, which is required before placing any plastic objects.
    # Non-plastic objects (object0, object2, object4) are placed without constraints.
    # The plastic object (object3) is placed after ensuring a compressible object is already in the box.
    # This sequence respects all given rules and achieves the goal state where all objects are packed in the box.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
