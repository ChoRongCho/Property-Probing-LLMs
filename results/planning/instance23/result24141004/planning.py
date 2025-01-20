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
    is_compressible: bool
    is_rigid: bool
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
        # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
        # Preconditions: The robot's hand must be empty, and the object must not already be in the bin.
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is a plastic object and if the constraint applies
        if obj.object_type == "plastic" and hasattr(obj, 'is_compressible'):
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return

        # If constraints are not applicable or satisfied, proceed to place the object
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. Hand must remain empty before and after the pushing.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is 3D and compressible
        if obj.is_3D and obj.is_compressible:
            # Ensure the robot's hand is empty before pushing
            if self.robot_handempty:
                print(f"push {obj.name}")
                # The effect of the action: the robot's hand remains empty
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name} because the robot's hand is not empty")
        else:
            print(f"Cannot push {obj.name} due to constraints not being met")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is foldable and not 3D
        if obj.is_foldable and not obj.is_3D:
            print(f"fold {obj.name}")
            # Effects: The robot's hand remains empty after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_foldable=False, is_3D=True)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_foldable=False, is_3D=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_foldable=False, is_3D=True)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_compressible=False, is_rigid=False, is_foldable=True, is_3D=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_foldable=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, object0.is_3D is True, actions pick, place, push are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_compressible is True, object2.is_3D is True, actions pick, place, push are applicable
    # object3.is_foldable is True, actions pick, place, fold are applicable
    # object4.is_compressible is True, object4.is_3D is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (yellow_2D_rectangle) since it is foldable.
    # 2. Pick and place object3 into the box.
    # 3. Pick and place object0 (yellow_3D_cuboid) into the box, then push it.
    # 4. Pick and place object2 (white_3D_cylinder) into the box, then push it.
    # 5. Pick and place object4 (red_3D_polyhedron) into the box, then push it.
    # 6. Pick and place object1 (blue_3D_cylinder) into the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing it, and push compressible objects after placing them.
    # Non-plastic objects are placed without additional constraints, and the sequence ensures all objects are packed as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
