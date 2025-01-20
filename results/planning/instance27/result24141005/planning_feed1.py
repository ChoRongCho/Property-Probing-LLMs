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
    is_compressible: bool
    is_rigid: bool

    # Additional predicates for bin_packing (max: 1)
    is_fragile: bool


@dataclass
class Box:
    # Basic dataclass
    index: int
    name: str

    # Predicates for box
    object_type: str  # box or obj
    in_bin_objects: list

# only write a code here without example instantiation
# Note! If a predicate required by the constraints is not defined in the class Object, ignore the constraints!!!
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
        # Preconditions: The object must not be in a box, the robot hand must be empty, and the object must not be fragile.
        if not obj.in_bin and self.robot_handempty and not obj.is_fragile:
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object, and the object must not already be in the box.
        if not self.robot_handempty and not obj.in_bin:
            # Check if the object is a box or obj
            if obj.object_type == "obj":
                # Check if the box already contains a compressible object
                compressible_present = any(o.is_compressible for o in box.in_bin_objects)
                
                # Constraint: If the object is compressible or a compressible object is present, place it
                if obj.is_compressible or compressible_present:
                    # Effects
                    print(f"place {obj.name}")
                    self.state_handempty()
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                else:
                    print(f"Cannot place {obj.name} due to missing compressible object")
            else:
                # If the object is a box, place it without constraints
                print(f"place {obj.name}")
                self.state_handempty()
                obj.in_bin = True
                box.in_bin_objects.append(obj)
        else:
            print(f"Cannot place {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and already in the box, and the robot's hand must be empty.
        if obj.is_compressible and obj.in_bin and self.robot_handempty:
            print(f"push {obj.name}")
            # Effect: The robot's hand remains empty after the push
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_fragile=False)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_fragile=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_fragile=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_rigid is True, actions pick, place are applicable
    # object3.is_compressible is True, actions pick, place, push are applicable
    # object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place a compressible object first to satisfy the rule for plastic objects.
    # 2. Push all compressible objects after placing them.
    # 3. Pick and place non-plastic objects without constraints.
    # 4. Ensure no bending or folding actions are needed as no objects are bendable or foldable.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box0', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts by placing compressible objects first (object0, object1, object3) to allow subsequent placement of any plastic objects if they existed.
    # Each compressible object is pushed after placement to ensure they are properly packed.
    # Non-compressible objects (object2, object4) are placed without additional constraints.
    # No bending or folding actions are required as none of the objects are bendable or foldable.

    # Finally, add this code    
    print("All task planning is done")

