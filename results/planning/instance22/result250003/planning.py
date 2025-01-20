from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # physical state of an object for {self.task}
    in_bin: bool

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
        # Action Description: Pick an object that is not in the box. 
        # The action does not include the 'place' action and can be applied to any type of object.
        
        # Preconditions: The object should not be in the bin, and the robot's hand should be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is not empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if compressible_present:
                # Action Description: Place a plastic object into the box if a compressible object is present.
                print(f"place {obj.name}")
                # Update the state to reflect the object is now in the box
                box.in_bin_objects.append(obj)
                self.state_handempty()
            else:
                print(f"Cannot place {obj.name}")
        else:
            # Action Description: Place a non-plastic object into the box without constraints.
            print(f"place {obj.name}")
            # Update the state to reflect the object is now in the box
            box.in_bin_objects.append(obj)
            self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0: is_rigid = True, is_foldable = False, is_compressible = False
    # object1: is_rigid = True, is_foldable = True, is_compressible = False
    # object2: is_rigid = True, is_foldable = False, is_compressible = False
    # object3: is_rigid = True, is_foldable = False, is_compressible = True

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object1 (if foldable)
    # 2. Pick object1
    # 3. Place object1
    # 4. Pick object3
    # 5. Place object3
    # 6. Push object3 (if compressible)
    # 7. Pick object0
    # 8. Place object0
    # 9. Pick object2
    # 10. Place object2

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object1 if foldable
    if hasattr(object1, 'is_foldable') and object1.is_foldable:
        action.fold(object1, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object3, then push if compressible
    action.pick(object3, box)
    action.place(object3, box)
    if hasattr(object3, 'is_compressible') and object3.is_compressible:
        action.push(object3, box)

    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold before picking, push after placing compressible objects,
    # and ensures that all objects are placed in the bin as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
