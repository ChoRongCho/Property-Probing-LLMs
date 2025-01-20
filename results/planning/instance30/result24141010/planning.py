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
    is_bendable: bool = False
    is_compressible: bool = False
    is_foldable: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_3D: bool = False


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
        # Preconditions: The object must not be in the bin, and the robot hand must be empty.
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
        
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name} because it is already in the bin.")
            return

        # Check the constraint: Before placing a plastic object, a compressible object should be in the box before.
        # Since 'plastic' is not a property in the Object class, this constraint is ignored.

        # Place the object in the box
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the bin
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state to hand empty
        self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable and not already in the bin
        if obj.is_bendable and not obj.in_bin:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            self.state_handempty()  # Ensure the hand is empty before bending
            print(f"bend {obj.name}")
            self.state_handempty()  # Ensure the hand is empty after bending
            # Additional effects can be added here if necessary, such as updating the object's state
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Check if the object is compressible and 3D, and ensure the robot's hand is empty
        if obj.is_compressible and obj.is_3D and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin. 
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Since the hand must remain empty, no state change is needed for the robot's hand
            # Effect: The object is considered pushed in the box
            # No additional state change for the box or object is specified
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not already in the bin
        if obj.is_foldable and not obj.in_bin:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: Hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True, actions pick, place are applicable
    # object1.is_compressible and is_3D are True, actions pick, place, push are applicable
    # object2.is_foldable is True, actions pick, place, fold are applicable
    # object3.is_bendable is True, actions pick, place, bend are applicable
    # object4.is_compressible and is_3D are True, actions pick, place, push are applicable
    # object5.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 (black_1D_line) before placing it.
    # 2. Fold object2 (transparent_2D_circle) before placing it.
    # 3. Place object1 (white_3D_cylinder) as it is compressible.
    # 4. Push object1 after placing it.
    # 5. Place object4 (red_3D_polyhedron) as it is compressible.
    # 6. Push object4 after placing it.
    # 7. Place object0 (blue_3D_cylinder) and object5 (green_3D_cylinder) as they are rigid.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before placing bendable and foldable objects.
    # Compressible objects are pushed after being placed in the bin.
    # Non-plastic objects are placed without constraints.
    # The sequence ensures all objects reach their goal state of being in the bin.

    # Finally, add this code    
    print("All task planning is done")
