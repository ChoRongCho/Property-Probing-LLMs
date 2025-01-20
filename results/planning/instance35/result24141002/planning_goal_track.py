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
    is_plastic: bool = False
    is_foldable: bool = False
    is_rigid: bool = False
    is_bendable: bool = False
    is_compressible: bool = False

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
        # Preconditions: The robot's hand must be empty, and the object must not be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is currently holding the object
        if self.robot_now_holding == obj:
            # Check if the object is plastic and ensure a compressible object is already in the box
            if obj.is_plastic:
                compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
                if not compressible_in_box:
                    print(f"Cannot place {obj.name} because no compressible object is in the box.")
                    return
            
            # Place the object in the box
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()  # Update the robot's state to hand empty
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name} because the robot is not holding it.")

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            print(f"bend {obj.name}")
            # Ensure the robot's hand is empty before and after bending
            self.state_handempty()
            # No change in the state of the box or object is required for bending
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after the action.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Ensure the robot's hand is empty before and after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_plastic is True, actions pick, place are applicable (with constraints)
    # object1.is_foldable is True, actions pick, place, fold are applicable
    # object2.is_rigid is True, actions pick, place are applicable
    # object3.is_bendable is True, actions pick, place, bend are applicable
    # object4.is_compressible is True, actions pick, place, push are applicable
    # object5.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object1 (foldable)
    # 2. Bend object3 (bendable)
    # 3. Pick and place object4 (compressible), then push
    # 4. Pick and place object1 (folded)
    # 5. Pick and place object3 (bent)
    # 6. Pick and place object0 (plastic, after compressible is in the box)
    # 7. Pick and place object2 (rigid)
    # 8. Pick and place object5 (rigid)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object1, box)
    action.bend(object3, box)
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.pick(object3, box)
    action.place(object3, box)
    action.pick(object0, box)
    action.place(object0, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before picking and placing.
    # A compressible object is placed and pushed before placing the plastic object.
    # All objects are placed in the box according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4, object5]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
