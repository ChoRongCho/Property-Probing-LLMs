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
    is_foldable: bool
    is_compressible: bool
    
    # Additional predicates for bin_packing (max: 1)
    is_3D: bool


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
        # Preconditions: The object is not in the bin, and the robot's hand is empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, already in bin.")
            return

        # Check if the object is a plastic object and if the constraint applies
        if obj.object_type == "plastic" and obj.is_compressible:
            # Check if there's at least one compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}, no compressible object in box.")
                return

        # Place the object in the box
        print(f"place {obj.name}")
        obj.in_bin = True
        box.in_bin_objects.append(obj)

        # Update the robot's state
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and 3D, and not plastic
        if obj.is_compressible and obj.is_3D and obj.object_type != "plastic":
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Ensure the robot's hand is empty before and after the action
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and is not a plastic object
        if obj.is_foldable and obj.object_type != "plastic":
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Ensure the robot's hand is empty before folding
            self.state_handempty()
            # Fold the object (no actual state change in this simplified example)
            # Ensure the robot's hand is empty after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_foldable=False, is_compressible=True, is_3D=True)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True, is_compressible=False, is_3D=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True, is_compressible=False, is_3D=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_foldable=False, is_compressible=True, is_3D=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_foldable=False, is_compressible=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_compressible is True, is_3D is True, actions pick, place, push are applicable
    # object1: is_foldable is True, actions pick, place, fold are applicable
    # object2: is_foldable is True, actions pick, place, fold are applicable
    # object3: is_compressible is True, is_3D is True, actions pick, place, push are applicable
    # object4: is_compressible is True, is_3D is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object1, pick object1, place object1
    # 2. Fold object2, pick object2, place object2
    # 3. Pick object0, place object0, push object0
    # 4. Pick object3, place object3, push object3
    # 5. Pick object4, place object4, push object4

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold and place object1
    action.fold(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    # Fold and place object2
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    # Place and push object0
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    # Place and push object3
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    # Place and push object4
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: foldable objects are folded before placing, compressible objects are pushed after placing, and no actions are performed on plastic objects. The order ensures that a compressible object is placed first, allowing subsequent plastic objects to be placed without constraint violations.

    # Finally, add this code    
    print("All task planning is done")
