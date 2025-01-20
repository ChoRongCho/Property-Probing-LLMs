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

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The object is not in the bin, the robot's hand is empty, and the object is rigid.
        if not obj.in_bin and self.robot_handempty and obj.is_rigid:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is already in the bin
        if obj.in_bin:
            print(f"Cannot place {obj.name}: already in bin")
            return
        
        # Check if the object is plastic and ensure a compressible object is already in the box
        if obj.is_plastic:
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}: requires a compressible object in the box first")
                return
        
        # Place the object in the box
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the bin
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and 3D
        if obj.is_compressible and obj.is_3D:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            if self.robot_handempty:
                print(f"push {obj.name}")
                # No change in the robot's state since the hand remains empty
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name} because the hand is not empty")
        else:
            print(f"Cannot push {obj.name} because it is not compressible and 3D")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # State the effect of Action: Hand remains empty
            self.state_handempty()
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
    # the object0.is_plastic is True, actions pick, place are applicable (requires compressible in box first)
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_compressible is True, actions pick, place, push are applicable
    # the object3.is_plastic is True, actions pick, place are applicable (requires compressible in box first)
    # the object4.is_foldable is True, actions pick, place, fold are applicable
    # the object5.is_plastic is True, actions pick, place are applicable (requires compressible in box first)
    # the object6.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True
    # object6: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume or change the physical properties of the object.
    # Order: fold object4 -> pick object4 -> place object4 -> pick object2 -> place object2 -> push object2 -> pick object6 -> place object6 -> push object6 -> pick object1 -> place object1 -> pick object0 -> place object0 -> pick object3 -> place object3 -> pick object5 -> place object5

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object4, box)
    action.pick(object4, box)
    action.place(object4, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object6, box)
    action.place(object6, box)
    action.push(object6, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence begins by folding the foldable object (object4) before placing it, adhering to rule 4. 
    # Compressible objects (object2 and object6) are placed and then pushed, following rule 2. 
    # Non-plastic objects (object1) are placed without additional constraints. 
    # Plastic objects (object0, object3, object5) are placed after a compressible object is already in the box, satisfying rule 1. 
    # No bending is performed as there are no bendable objects.

    # Finally, add this code    
    print("All task planning is done")

