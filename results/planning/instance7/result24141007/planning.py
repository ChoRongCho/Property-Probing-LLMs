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
    is_plastic: bool
    
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

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The object is not in the bin, and the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the object is considered in the bin
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if a compressible object is already in the box
        if obj.is_plastic:
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Preconditions are satisfied, proceed with placing the object
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check preconditions: the object must be compressible and the robot's hand must be empty
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
            
            # Effects: The robot's hand remains empty after pushing
            self.state_handempty()
            
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=False, is_plastic=True, is_heavy=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_plastic=False, is_heavy=False)
object2 = Object(index=2, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_compressible=False, is_plastic=True, is_heavy=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_plastic=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_plastic is True, is_compressible is False, actions pick, place are applicable
    # object1: is_compressible is True, actions pick, place, push are applicable
    # object2: is_plastic is True, is_compressible is False, actions pick, place are applicable
    # object3: is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object1 (compressible), then push it.
    # 2. Pick and place object3 (compressible), then push it.
    # 3. Pick and place object0 (plastic), since a compressible object is already in the box.
    # 4. Pick and place object2 (plastic), since a compressible object is already in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts by placing compressible objects first (object1 and object3) and pushing them,
    # ensuring that the condition for placing plastic objects (object0 and object2) is met.
    # This follows the rule that a compressible object must be in the box before placing any plastic object.
    # The actions are performed in a sequence that respects the constraints and ensures all objects are packed.

    # Finally, add this code    
    print("All task planning is done")
