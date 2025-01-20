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
    is_3D: bool = False


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
        self.robot_now_holding = None

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The object must not be in the bin, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object, and the object must not be in the bin.
        if not self.robot_handempty and self.robot_now_holding == obj and not obj.in_bin:
            if obj.is_plastic:
                # Ensure there's at least one compressible object in the box
                if any(o.is_compressible for o in box.in_bin_objects):
                    print(f"place {obj.name}")
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} - no compressible object in the box")
            else:
                # Non-plastic objects can be placed without constraints
                print(f"place {obj.name}")
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name} - preconditions not met")

    def push(self, obj, box):
        # Check if the object is compressible and 3D, and already in the bin
        if obj.is_compressible and obj.is_3D and obj.in_bin:
            if self.robot_handempty:
                print(f"push {obj.name}")
            else:
                print(f"Cannot push {obj.name} because the robot is holding something")
        else:
            print(f"Cannot push {obj.name} because it is not compressible and 3D or not in the bin")

    def fold(self, obj, box):
        if self.robot_handempty and obj.is_foldable and not obj.is_3D:
            print(f"fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_plastic=True)
object2 = Object(index=2, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_foldable=True)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True and object0.is_3D is True, actions pick, place are applicable
    # object1.is_plastic is True, actions pick, place are applicable
    # object2.is_foldable is True, actions pick, place, fold are applicable
    # object3.is_foldable is True, actions pick, place, fold are applicable
    # object4.is_compressible is True and object4.is_3D is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object2 (yellow_2D_rectangle) before placing it.
    # 2. Fold object3 (transparent_2D_circle) before placing it.
    # 3. Place object4 (brown_3D_cylinder) first as it is compressible.
    # 4. Place object0 (white_3D_cuboid) as it has no constraints.
    # 5. Place object2 (yellow_2D_rectangle) after folding.
    # 6. Place object3 (transparent_2D_circle) after folding.
    # 7. Place object1 (blue_2D_rectangle) after a compressible object is in the box.
    # 8. Push object4 (brown_3D_cylinder) after placing it.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold foldable objects before placing, place a compressible object before a plastic one, and push compressible objects after placing. 
    # The sequence ensures that all objects are placed in the box according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")

