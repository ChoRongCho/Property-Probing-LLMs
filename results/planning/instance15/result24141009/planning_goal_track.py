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
    is_bendable: bool
    is_plastic: bool

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
        # Preconditions: The robot's hand must be empty, and the object must not already be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
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
        
        # Preconditions are satisfied, proceed with placing the object
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state to hand empty
        self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            if self.robot_handempty:
                print(f"bend {obj.name}")
                # Effects: The robot's hand remains empty after bending
                self.state_handempty()
            else:
                print(f"Cannot bend {obj.name} because the hand is not empty")
        else:
            print(f"Cannot bend {obj.name} because it is not bendable or is plastic")

    def push(self, obj, box):
        # Preconditions: The object must be compressible and in the bin, and the robot's hand must be empty.
        if obj.is_compressible and obj.in_bin and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_compressible=False, is_bendable=False, is_plastic=False, is_heavy=False)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_bendable=False, is_plastic=False, is_heavy=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_bendable=False, is_plastic=False, is_heavy=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_bendable=False, is_plastic=True, is_heavy=False)
object4 = Object(index=4, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_compressible=False, is_bendable=True, is_plastic=False, is_heavy=False)
object5 = Object(index=5, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_compressible=True, is_bendable=False, is_plastic=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, actions pick, place are applicable
    # object1: is_compressible is True, actions pick, place, push are applicable
    # object2: is_compressible is True, actions pick, place, push are applicable
    # object3: is_plastic is True, actions pick, place are applicable (requires compressible object in box first)
    # object4: is_bendable is True, actions pick, place, bend are applicable
    # object5: is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object4 (black_1D_line) before placing it.
    # 2. Pick and place object1 (yellow_3D_cuboid) as it is compressible.
    # 3. Push object1 after placing it.
    # 4. Pick and place object2 (white_3D_cylinder) as it is compressible.
    # 5. Push object2 after placing it.
    # 6. Pick and place object5 (brown_3D_cylinder) as it is compressible.
    # 7. Push object5 after placing it.
    # 8. Pick and place object3 (blue_2D_rectangle) after a compressible object is in the box.
    # 9. Pick and place object0 (white_3D_cuboid).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object4, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)
    action.pick(object5, box)
    action.place(object5, box)
    action.push(object5, box)
    action.pick(object3, box)
    action.place(object3, box)
    action.pick(object0, box)
    action.place(object0, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by bending the bendable object before placing it.
    # Compressible objects are placed and pushed immediately after placement.
    # The plastic object is placed only after a compressible object is in the box.
    # Non-plastic, non-compressible objects are placed without additional actions.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4, object5]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
