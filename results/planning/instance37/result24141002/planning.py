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
    is_rigid: bool = False
    is_compressible: bool = False
    is_plastic: bool = False
    is_bendable: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_fragile: bool = False


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
        # Preconditions: The object is not in the bin and the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic:
            # Check if there is a compressible object already in the box
            compressible_present = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return

        # If constraints are not applicable or satisfied, proceed with placing the object
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # Ensure the robot's hand is empty before and after the action
            self.state_handempty()
            # Additional effects can be added here if necessary
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. Hand must remain empty before and after the pushing.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is compressible and not plastic
        if obj.is_compressible and not obj.is_plastic:
            print(f"push {obj.name}")
            # Ensure the robot's hand is empty before and after the push
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            print(f"fold {obj.name}")
            # Assuming the robot's hand must be empty before and after folding
            self.state_handempty()
            # No change in holding state as folding does not require holding the object
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True)
object5 = Object(index=5, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_foldable is True, actions pick, place, fold are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_bendable is True, actions pick, place, bend are applicable
    # the object3.is_plastic is True, actions pick, place are applicable
    # the object4.is_compressible is True, actions pick, place, push are applicable
    # the object5.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 (foldable) -> pick -> place
    # 2. Bend object2 (bendable) -> pick -> place
    # 3. Pick object4 (compressible) -> place -> push
    # 4. Pick object5 (compressible) -> place -> push
    # 5. Pick object3 (plastic) -> place (after a compressible object is in the box)
    # 6. Pick object1 (rigid) -> place

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object0, box)
    action.pick(object0, box)
    action.place(object0, box)

    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object5, box)
    action.place(object5, box)
    action.push(object5, box)

    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before picking and placing.
    # Compressible objects are pushed after placing. A plastic object is placed only after a compressible object is in the box.
    # The sequence ensures all objects are packed according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")
