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
    is_compressible: bool = False
    is_plastic: bool = False
    is_bendable: bool = False
    is_rigid: bool = False

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
        # Preconditions: The object is not in the bin, and the robot's hand is empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
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

        # If constraints are satisfied or not applicable, proceed to place the object
        print(f"place {obj.name}")
        self.state_handempty()  # Assuming the robot hand becomes empty after placing the object
        box.in_bin_objects.append(obj)  # Add the object to the box
        obj.in_bin = True  # Update the object's state to reflect it is now in the bin

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and obj.is_bendable and not obj.is_plastic:
            print(f"bend {obj.name}")
            # Effect: The object is bent, but the robot's hand remains empty.
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Check if the object is compressible and 3D
        if obj.is_compressible and obj.is_3D:
            # Preconditions: Robot hand must be empty and the object must be in the bin
            if self.robot_handempty and obj.in_bin:
                print(f"push {obj.name}")
                # Effects: The robot hand remains empty after pushing
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name}: Preconditions not met (hand must be empty and object must be in the bin)")
        else:
            print(f"Cannot push {obj.name}: Object is not compressible and 3D")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_compressible is True and object0.is_3D is True, actions pick, place, push are applicable
    # the object1.is_plastic is True, actions pick, place are applicable (with constraints)
    # the object2.is_bendable is True, actions pick, bend, place are applicable
    # the object3.is_compressible is True and object3.is_3D is True, actions pick, place, push are applicable
    # the object4.is_rigid is True and object4.is_3D is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (black_1D_line) since it's bendable.
    # 2. Pick and place object0 (yellow_3D_cuboid) since it's compressible and 3D.
    # 3. Push object0 after placing it.
    # 4. Pick and place object3 (red_3D_polyhedron) since it's compressible and 3D.
    # 5. Push object3 after placing it.
    # 6. Pick and place object1 (blue_2D_rectangle) since a compressible object is already in the box.
    # 7. Pick and place object4 (green_3D_cylinder) since it's rigid and 3D.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name="box1", object_type="box", in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)  # Bend the bendable object
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)  # Push the compressible object
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)  # Push the compressible object
    action.pick(object1, box)
    action.place(object1, box)  # Place the plastic object after compressible
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object first, place a compressible object before a plastic one,
    # and push compressible objects after placing them. The sequence ensures all objects are placed in the box
    # according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")
