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
    is_heavy: bool


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
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: Update the state to reflect that the robot is now holding the object
            self.state_holding(obj)
            # Optionally, update the box's list of in_bin_objects if needed
            # box.in_bin_objects.append(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is a plastic object and if the constraint applies
        if obj.object_type == "plastic" and obj.is_compressible:
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Place the object in the box
        print(f"place {obj.name}")
        box.in_bin_objects.append(obj)
        
        # Update the state of the robot
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and not plastic (assuming plastic is determined by color or material, which is not in the class)
        if obj.is_compressible and not obj.is_foldable:
            # Action Description: Push a 3D compressible object downward in the bin. Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Ensure the robot's hand is empty before and after the action
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Since folding doesn't require holding the object, ensure the hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_foldable=False, is_compressible=True, is_heavy=False)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True, is_compressible=False, is_heavy=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True, is_compressible=False, is_heavy=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_foldable=False, is_compressible=True, is_heavy=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_foldable=False, is_compressible=True, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_foldable is True, actions pick, place, fold are applicable
    # object2.is_foldable is True, actions pick, place, fold are applicable
    # object3.is_compressible is True, actions pick, place, push are applicable
    # object4.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object1 (yellow_2D_rectangle) and object2 (transparent_2D_circle) before placing.
    # 2. Pick and place object0 (yellow_3D_cuboid), object3 (red_3D_polyhedron), and object4 (brown_3D_cylinder) as they are compressible.
    # 3. Push object0, object3, and object4 after placing them in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box0', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold foldable objects
    action.fold(object1, box)
    action.fold(object2, box)

    # Pick and place compressible objects
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Pick and place foldable objects
    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold foldable objects before placing, place compressible objects and push them after placing.
    # Non-plastic objects are placed without additional constraints. The sequence ensures all objects are packed as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
