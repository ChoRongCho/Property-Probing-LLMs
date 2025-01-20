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
    is_plastic: bool
    is_rigid: bool
    is_compressible: bool
    is_foldable: bool

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
        # Check if the object is plastic and ensure a compressible object is already in the box
        if obj.is_plastic:
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state to hand empty after placing the object
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check preconditions: the object must be compressible and the robot's hand must be empty
        if obj.is_compressible and self.robot_handempty:
            # Action Description: Push a 3D compressible object downward in the bin. 
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            
            # Effect: The object is now considered in the bin
            obj.in_bin = True
            
            # Ensure the robot's hand remains empty after the action
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable
        if obj.is_foldable:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            if self.robot_handempty:
                print(f"fold {obj.name}")
                # Effect: The robot's hand remains empty after folding
                self.state_handempty()
            else:
                print(f"Cannot fold {obj.name} because the hand is not empty")
        else:
            print(f"Cannot fold {obj.name} because it is not foldable")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_compressible=False, is_foldable=False, is_heavy=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=True, is_compressible=False, is_foldable=False, is_heavy=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=False, is_compressible=True, is_foldable=False, is_heavy=False)
object3 = Object(index=3, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_compressible=False, is_foldable=False, is_heavy=False)
object4 = Object(index=4, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=False, is_rigid=False, is_compressible=False, is_foldable=True, is_heavy=False)
object5 = Object(index=5, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True, is_rigid=False, is_compressible=False, is_foldable=False, is_heavy=False)
object6 = Object(index=6, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_plastic=False, is_rigid=False, is_compressible=True, is_foldable=False, is_heavy=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_plastic is True, object0.is_compressible is False, actions pick, place are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable
    # object3.is_plastic is True, object3.is_compressible is False, actions pick, place are applicable
    # object4.is_foldable is True, actions pick, place, fold are applicable
    # object5.is_plastic is True, object5.is_compressible is False, actions pick, place are applicable
    # object6.is_compressible is True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True
    # object6: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object2 (compressible) into the box, then push it.
    # 2. Pick and place object6 (compressible) into the box, then push it.
    # 3. Fold object4 (foldable), pick and place it into the box.
    # 4. Pick and place object1 (rigid) into the box.
    # 5. Pick and place object0 (plastic) into the box (after compressible objects are in).
    # 6. Pick and place object3 (plastic) into the box (after compressible objects are in).
    # 7. Pick and place object5 (plastic) into the box (after compressible objects are in).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name="box1", object_type="box", in_bin_objects=[])

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
    # The sequence starts with placing compressible objects (object2 and object6) to satisfy the rule for placing plastic objects.
    # Object4 is folded before placing due to its foldable property.
    # Object1 is placed without constraints as it is non-plastic and non-compressible.
    # Plastic objects (object0, object3, object5) are placed after compressible objects are in the box.
    # The sequence respects all given rules and achieves the goal state.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4, object5, object6]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
