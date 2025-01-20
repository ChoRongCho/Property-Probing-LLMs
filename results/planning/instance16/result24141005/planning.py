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
        # Preconditions: The robot's hand must be empty, and the object must not already be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. 
            # The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Preconditions: The robot must be holding the object and the object must not already be in a bin.
        if self.robot_now_holding == obj and not obj.in_bin:
            # Since the constraint mentions a "plastic" object, and there's no attribute for material type in the Object class,
            # we ignore the constraint about placing a plastic object after a compressible one.
            
            # Effect: Place the object in the box and update states
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            self.state_handempty()
            
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check preconditions: the object must be compressible and the robot's hand must be empty
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin. Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after the action
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is foldable and is not already in the bin
        if self.robot_handempty and not obj.in_bin and obj.is_foldable and not obj.is_3D:
            print(f"fold {obj.name}")
            # Update the state to reflect that the object has been folded
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_foldable=False, is_3D=True)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_3D=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_3D=True)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_foldable=True, is_3D=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_foldable=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid=True, is_compressible=False, is_foldable=False, is_3D=True
    #          Actions: pick, place
    # object1: is_rigid=False, is_compressible=True, is_foldable=False, is_3D=True
    #          Actions: pick, place, push
    # object2: is_rigid=False, is_compressible=True, is_foldable=False, is_3D=True
    #          Actions: pick, place, push
    # object3: is_rigid=False, is_compressible=False, is_foldable=True, is_3D=False
    #          Actions: pick, place, fold
    # object4: is_rigid=False, is_compressible=True, is_foldable=False, is_3D=True
    #          Actions: pick, place, push

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (yellow_2D_rectangle) before placing it.
    # 2. Pick and place object1 (yellow_3D_cuboid) as it is compressible.
    # 3. Push object1 after placing it.
    # 4. Pick and place object2 (white_3D_cylinder) as it is compressible.
    # 5. Push object2 after placing it.
    # 6. Pick and place object4 (brown_3D_cylinder) as it is compressible.
    # 7. Push object4 after placing it.
    # 8. Pick and place object3 (yellow_2D_rectangle) after folding.
    # 9. Pick and place object0 (white_3D_cuboid) as it is non-plastic and can be placed without constraints.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)
    action.pick(object3, box)
    action.place(object3, box)
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, place compressible objects first,
    # and push them after placing. Non-plastic objects can be placed without constraints. The sequence ensures
    # all objects are packed according to their properties and the given rules.

    # Finally, add this code    
    print("All task planning is done")
