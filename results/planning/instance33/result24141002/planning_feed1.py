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
    is_fragile: bool


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
        # Preconditions: The robot's hand must be empty, and the object must not already be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is plastic and ensure a compressible object is already in the box
        if obj.is_plastic:
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Preconditions: The robot must be holding the object
        if self.robot_now_holding == obj:
            print(f"place {obj.name}")
            
            # Effects: Update the state to reflect the object is now in the bin and the robot hand is empty
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check preconditions: the object must be compressible, in the box, and the robot's hand must be empty
        if obj.is_compressible and obj.in_bin and self.robot_handempty:
            print(f"push {obj.name}")
            # Effect: The robot's hand remains empty after pushing
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_plastic=False, is_fragile=False)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_plastic=False, is_fragile=False)
object2 = Object(index=2, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_plastic=True, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_plastic is True, actions pick, place are applicable (with constraint)

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object0 (compressible), then push it.
    # 2. Pick and place object1 (rigid).
    # 3. Pick and place object2 (plastic), ensuring object0 is already in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Step 1: Pick and place object0, then push it
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    # Step 2: Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Step 3: Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: object0 is placed first because it is compressible and needs to be pushed.
    # object1 is placed next as it has no constraints.
    # object2 is placed last because it is plastic and requires a compressible object (object0) to be in the box first.

    # Finally, add this code    
    print("All task planning is done")

