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
        # Preconditions: The object must not be in the box, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}, it is already in the bin.")
            return
        
        # Check if the object is a plastic object and if the constraint applies
        if obj.object_type == "plastic" and obj.is_compressible:
            # Check if there is at least one compressible object already in the box
            if not any(o.is_compressible for o in box.in_bin_objects):
                print(f"Cannot place {obj.name}, no compressible object in the box.")
                return
        
        # Place the object in the box
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the bin
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state to hand empty
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and 3D, and ensure it's not plastic
        if obj.is_compressible and obj.is_3D and obj.object_type != "plastic":
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effects: Ensure the robot's hand is empty after the action
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and is not 3D
        if hasattr(obj, 'is_foldable') and obj.is_foldable and hasattr(obj, 'is_3D') and not obj.is_3D:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Ensure the robot's hand is empty before and after folding
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
    # the object0.is_compressible is True, actions pick, place, push are applicable
    # the object1.is_foldable is True, actions pick, place, fold are applicable
    # the object2.is_foldable is True, actions pick, place, fold are applicable
    # the object3.is_compressible is True, actions pick, place, push are applicable
    # the object4.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume or change the physical properties of the object.
    # 1. Fold object1 (yellow_2D_rectangle) -> Pick -> Place
    # 2. Fold object2 (transparent_2D_circle) -> Pick -> Place
    # 3. Pick object0 (yellow_3D_cuboid) -> Place -> Push
    # 4. Pick object3 (red_3D_polyhedron) -> Place -> Push
    # 5. Pick object4 (brown_3D_cylinder) -> Place -> Push

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts with folding the foldable objects (object1 and object2) before picking and placing them in the box.
    # This ensures compliance with the rule that foldable objects must be folded before placement.
    # Next, compressible objects (object0, object3, and object4) are picked, placed, and then pushed in the box.
    # This follows the rule that compressible objects must be pushed after placement.
    # The sequence respects all constraints, ensuring no plastic objects are bent, folded, or pushed.

    # Finally, add this code    
    print("All task planning is done")
