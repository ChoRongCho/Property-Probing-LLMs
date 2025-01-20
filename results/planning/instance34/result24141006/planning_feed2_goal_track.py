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
    is_bendable: bool

    # Additional predicates for bin_packing (max: 1)
    is_heavy: bool


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
        # Preconditions: The robot's hand must be empty, and the object must not be in a box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object.
        if self.robot_now_holding == obj:
            # Place the object in the box
            print(f"place {obj.name}")
            # Effects: The object is now in the bin, and the robot hand is empty
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and already in the bin.
        if obj.is_compressible and obj.in_bin:
            print(f"push {obj.name}")
            # Effects: Hand remains empty after pushing
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def bend(self, obj, box):
        # Preconditions: The object must be bendable.
        if obj.is_bendable:
            print(f"bend {obj.name}")
            # Effects: Hand remains empty after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_heavy=False)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_bendable=True, is_heavy=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_compressible is True, actions pick, place, push are applicable
    # object1: is_bendable is True, actions pick, place, bend are applicable
    # object2: is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object0 (compressible), then push it.
    # 2. Bend object1, then pick and place it.
    # 3. Pick and place object2 (compressible), then push it.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box0', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Step 1: Handle object0
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    # Step 2: Handle object1
    action.bend(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    # Step 3: Handle object2
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: 
    # - object0 is compressible, so it is placed first and pushed.
    # - object1 is bendable, so it is bent before being picked and placed.
    # - object2 is compressible, so it is placed last and pushed.
    # All objects are placed in the box according to the goal state.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
