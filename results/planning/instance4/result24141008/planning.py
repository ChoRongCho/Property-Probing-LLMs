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
    is_foldable: bool = False
    is_plastic: bool = False

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
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if there is a compressible object already in the box
        if obj.is_plastic:
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Preconditions: The robot must be holding the object and the object must not already be in a bin
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
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.is_3D and obj.is_compressible:
            print(f"push {obj.name}")
            # No change in robot's state is needed as the hand remains empty
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not already in the bin
        if obj.is_foldable and not obj.in_bin:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_3D=True)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object2 = Object(index=2, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_plastic is True, is_3D is True, actions pick, place are applicable
    # object1: is_compressible is True, is_3D is True, actions pick, place, push are applicable
    # object2: is_rigid is True, is_3D is True, actions pick, place are applicable
    # object3: is_foldable is True, actions pick, place, fold are applicable
    # object4: is_compressible is True, is_3D is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (yellow_2D_rectangle) before picking and placing it.
    # 2. Pick and place object1 (yellow_3D_cuboid) as it is compressible.
    # 3. Push object1 after placing it in the box.
    # 4. Pick and place object4 (brown_3D_cylinder) as it is compressible.
    # 5. Push object4 after placing it in the box.
    # 6. Pick and place object0 (red_3D_cuboid) after a compressible object is in the box.
    # 7. Pick and place object2 (blue_3D_cylinder) as it has no constraints.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, ensure a compressible object is in the box before placing a plastic object, and push compressible objects after placing them. Non-plastic objects can be placed without constraints.

    # Finally, add this code    
    print("All task planning is done")
