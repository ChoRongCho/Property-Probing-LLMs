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
    is_foldable: bool
    is_plastic: bool

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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and its hand is no longer empty.
            self.state_holding(obj)
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
        
        # Preconditions: The robot must be holding the object and the object should not already be in the bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Effect: Place the object in the box
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and 3D
        if obj.is_compressible and obj.is_3D:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            if self.robot_handempty:
                print(f"push {obj.name}")
                # No change in hand state as the hand must remain empty
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name} because the robot hand is not empty.")
        else:
            print(f"Cannot push {obj.name} because it is not compressible and 3D.")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        if self.robot_handempty and not obj.in_bin and obj.is_foldable and not obj.is_3D:
            print(f"fold {obj.name}")
            self.state_handempty()  # Ensure the hand remains empty after folding
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=False, is_plastic=True, is_3D=True)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_foldable=False, is_plastic=False, is_3D=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_plastic=False, is_3D=True)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=False, is_plastic=True, is_3D=False)
object4 = Object(index=4, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=True, is_plastic=False, is_3D=False)
object5 = Object(index=5, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=False, is_plastic=True, is_3D=False)
object6 = Object(index=6, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_plastic=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_plastic is True, is_3D is True, actions pick, place are applicable
    # object1: is_rigid is True, is_3D is True, actions pick, place are applicable
    # object2: is_compressible is True, is_3D is True, actions pick, place, push are applicable
    # object3: is_plastic is True, is_3D is False, actions pick, place are applicable
    # object4: is_foldable is True, is_3D is False, actions pick, place, fold are applicable
    # object5: is_plastic is True, is_3D is False, actions pick, place are applicable
    # object6: is_compressible is True, is_3D is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True
    # object6: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object2 (compressible)
    # 2. Push object2
    # 3. Pick and place object6 (compressible)
    # 4. Push object6
    # 5. Fold object4
    # 6. Pick and place object4
    # 7. Pick and place object1 (non-plastic)
    # 8. Pick and place object0 (plastic, after compressible objects are in the box)
    # 9. Pick and place object3 (plastic, after compressible objects are in the box)
    # 10. Pick and place object5 (plastic, after compressible objects are in the box)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object6, box)
    action.place(object6, box)
    action.push(object6, box)

    action.fold(object4, box)
    action.pick(object4, box)
    action.place(object4, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by ensuring compressible objects are placed and pushed first.
    # Foldable objects are folded before placement. Plastic objects are placed after compressible objects are in the box.
    # Non-plastic objects are placed without additional constraints.

    # Finally, add this code    
    print("All task planning is done")
