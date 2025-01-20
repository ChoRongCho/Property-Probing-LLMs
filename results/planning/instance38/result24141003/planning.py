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
    is_foldable: bool = False
    is_bendable: bool = False
    is_compressible: bool = False
    is_rigid: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_packable: bool = True


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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. 
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the robot is holding the object
        if self.robot_now_holding == obj:
            # Check if the object is packable
            if obj.is_packable:
                # Check if the object is a plastic object and if a compressible object is already in the box
                if obj.object_type == "plastic" and not any(o.is_compressible for o in box.in_bin_objects):
                    print(f"Cannot place {obj.name}")
                else:
                    # Place the object in the box
                    box.in_bin_objects.append(obj)
                    obj.in_bin = True
                    self.state_handempty()
                    print(f"place {obj.name}")
            else:
                print(f"Cannot place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Check if the object is bendable and not already in the bin
        if obj.is_bendable and not obj.in_bin:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # State the effect of Action: Hand remains empty after bending
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check preconditions: object must be compressible and robot hand must be empty
        if obj.is_compressible and self.robot_handempty:
            print(f"push {obj.name}")
            # Effect: The object is now considered pushed, and the robot hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and the robot's hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: The robot's hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_foldable is True, actions pick, place, fold are applicable
    # object1.is_bendable is True, actions pick, place, bend are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable
    # object3.is_rigid is True, actions pick, place are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 (transparent_2D_circle) before picking and placing it.
    # 2. Bend object1 (black_1D_line) before picking and placing it.
    # 3. Pick and place object2 (red_3D_polyhedron), then push it.
    # 4. Pick and place object3 (green_3D_cylinder).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object0
    action.fold(object0, box)
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Bend object1
    action.bend(object1, box)
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object2, then push
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before picking and placing.
    # The compressible object is pushed after being placed.
    # The order ensures that all objects are packed according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")
