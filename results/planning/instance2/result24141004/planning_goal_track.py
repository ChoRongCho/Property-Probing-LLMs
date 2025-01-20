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
    is_compressible: bool = False
    is_bendable: bool = False
    is_plastic: bool = False

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

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The object is not in the bin, the robot hand is empty, and the object is not heavy.
        if not obj.in_bin and self.robot_handempty and not obj.is_heavy:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint is applicable
        if obj.is_plastic:
            # Check if there is at least one compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return

        # If constraints are satisfied or not applicable, proceed with placing the object
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

    def bend(self, obj, box):
        # Action Description: Bend a 1D bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if obj.is_bendable and not obj.is_plastic and self.robot_handempty:
            print(f"bend {obj.name}")
            # State the effect of Action and box: self.state_holding or self.state_handempty etc if necessary
            self.state_handempty()  # Ensure the hand remains empty after bending
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        
        # Check preconditions: Object must be compressible and the robot's hand must be empty
        if obj.is_compressible and self.robot_handempty:
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
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True)
object1 = Object(index=1, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_plastic is True, actions pick, place are applicable (with constraints)
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_bendable is True, actions pick, place, bend are applicable
    # the object3.is_compressible is True, actions pick, place, push are applicable
    # the object4.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) before placing it.
    # 2. Pick and place object3 (red_3D_polyhedron), then push it.
    # 3. Pick and place object4 (brown_3D_cylinder), then push it.
    # 4. Pick and place object0 (red_3D_cuboid) after a compressible object is in the box.
    # 5. Pick and place object1 (white_3D_cuboid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)  # Bend the bendable object
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)  # Push the compressible object

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)  # Push the compressible object

    action.pick(object0, box)
    action.place(object0, box)  # Place the plastic object after a compressible one is in the box

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object first, place compressible objects and push them,
    # ensure a compressible object is in the box before placing a plastic object, and finally place the rigid object.
    # The robot's hand is empty before and after bending, folding, and pushing actions as required.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
