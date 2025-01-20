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
    is_plastic: bool = False
    is_rigid: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_heavy: bool = False


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
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic:
            # Check if there is a non-rigid object already in the box
            non_rigid_present = any(not o.is_rigid for o in box.in_bin_objects)
            if not non_rigid_present:
                print(f"Cannot place {obj.name}")
                return

        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state
        self.state_handempty()

        # Push all non-rigid, non-plastic objects after placing them in the box
        if not obj.is_rigid and not obj.is_plastic:
            self.push(obj, box)

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_heavy=False)
object1 = Object(index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False)
object2 = Object(index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_plastic is True, actions pick, place are applicable with constraints
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Since object0 is plastic, it requires a compressible object in the box first.
    # object1 and object2 can be placed without constraints.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Pick and place object1 (no constraints)
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object2 (no constraints)
    action.pick(object2, box)
    action.place(object2, box)

    # Now, object0 can be placed because there are objects in the box
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Object1 and object2 were placed first because they have no constraints and are not plastic.
    # Object0, being plastic, was placed last after ensuring the box already contained objects.
    # This sequence respects the rule that a plastic object requires a non-rigid object in the box first.
    # No bending, folding, or pushing actions were needed as none of the objects were bendable, foldable, or compressible.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
