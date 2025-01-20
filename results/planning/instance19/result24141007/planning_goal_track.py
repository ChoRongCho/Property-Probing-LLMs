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
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and its hand is no longer empty.
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
        
        # If the robot is holding the object and the object is not already in the bin
        if self.robot_now_holding == obj and not obj.in_bin:
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the bin
            obj.in_bin = True
            box.in_bin_objects.append(obj)
            # Update the robot's state to hand empty
            self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Preconditions: The object must be compressible, and the robot's hand must be empty.
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after the action.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and the robot's hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # No change in robot's state as hand remains empty
            # Effects: The object is now considered folded, but since there's no attribute for folded state, we assume it is ready for packing
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True, actions pick, place are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_foldable is True, actions pick, place, fold are applicable
    # object3.is_plastic is True, actions pick, place are applicable (with constraints)
    # object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object2 (foldable) before picking and placing.
    # 2. Pick and place object1 (compressible), then push it.
    # 3. Pick and place object2 (foldable).
    # 4. Pick and place object3 (plastic) after object1 (compressible) is in the box.
    # 5. Pick and place object0 (rigid).
    # 6. Pick and place object4 (rigid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)  # Fold object2
    action.pick(object1, box)  # Pick object1
    action.place(object1, box)  # Place object1
    action.push(object1, box)  # Push object1
    action.pick(object2, box)  # Pick object2
    action.place(object2, box)  # Place object2
    action.pick(object3, box)  # Pick object3
    action.place(object3, box)  # Place object3
    action.pick(object0, box)  # Pick object0
    action.place(object0, box)  # Place object0
    action.pick(object4, box)  # Pick object4
    action.place(object4, box)  # Place object4

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, ensure a compressible object is in the box before placing a plastic object, and push compressible objects after placing. Non-plastic, non-compressible, and non-foldable objects are simply picked and placed.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
