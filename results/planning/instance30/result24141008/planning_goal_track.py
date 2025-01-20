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
    is_bendable: bool
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
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the object is considered in the robot's possession.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is currently holding the object and the object is not already in a bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Check if the object is a plastic object and if the constraint applies
            if obj.object_type == "plastic":
                # Check if there is a compressible object already in the box
                if any(o.is_compressible for o in box.in_bin_objects):
                    print(f"place {obj.name}")
                    # Update the state to reflect the object is now in the bin
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} - No compressible object in the box")
            else:
                # For non-plastic objects, place without additional constraints
                print(f"place {obj.name}")
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name} - Not holding the object or already in bin")

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Preconditions: The object must be bendable, and the robot's hand must be empty.
        if obj.is_bendable and self.robot_handempty:
            print(f"bend {obj.name}")
            # Effects: The object is now bent, and the robot's hand remains empty.
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Preconditions: The object must be in the bin, compressible, and 3D.
        if obj.in_bin and obj.is_compressible and obj.is_3D:
            # Action Description: Push a 3D compressible object downward in the bin.
            # Hand must remain empty before and after the pushing.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty, no change in state needed.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
        if self.robot_handempty and obj.is_foldable and not obj.is_3D:
            print(f"fold {obj.name}")
            # Effects: The robot's hand remains empty after folding.
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_compressible=False, is_foldable=False, is_3D=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_compressible=True, is_foldable=False, is_3D=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_compressible=False, is_foldable=True, is_3D=False)
object3 = Object(index=3, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_rigid=False, is_bendable=True, is_compressible=False, is_foldable=False, is_3D=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_rigid=False, is_bendable=False, is_compressible=True, is_foldable=False, is_3D=True)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_bendable=False, is_compressible=False, is_foldable=False, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid=True, is_3D=True, actions: pick, place
    # object1: is_compressible=True, is_3D=True, actions: pick, place, push
    # object2: is_foldable=True, is_3D=False, actions: pick, place, fold
    # object3: is_bendable=True, is_3D=False, actions: pick, place, bend
    # object4: is_compressible=True, is_3D=True, actions: pick, place, push
    # object5: is_rigid=True, is_3D=True, actions: pick, place

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object3 before placing it.
    # 2. Fold object2 before placing it.
    # 3. Place object1 (compressible) in the box.
    # 4. Push object1.
    # 5. Place object4 (compressible) in the box.
    # 6. Push object4.
    # 7. Place object0 (non-plastic) in the box.
    # 8. Place object5 (non-plastic) in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend and fold actions are performed before picking and placing.
    # Compressible objects are pushed after being placed in the box.
    # Non-plastic objects are placed without additional constraints.
    # The sequence ensures all objects reach their goal state of being in the bin.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4, object5]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
