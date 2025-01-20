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
        # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
        if obj.in_bin and obj.object_type == "obj" and self.robot_handempty:
            print(f"pick {obj.name}")
            self.state_holding(obj)  # Effect: The robot is now holding the object
            box.in_bin_objects.remove(obj)  # Effect: Remove the object from the box's list of objects
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint is applicable
        if hasattr(obj, 'material') and obj.material == 'plastic':
            # Check if there is a compressible object already in the box
            compressible_present = any(
                hasattr(o, 'material') and o.material == 'compressible' for o in box.in_bin_objects
            )
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # If constraints are not applicable or satisfied, proceed to place the object
        print(f"place {obj.name}")
        self.state_handempty()  # Assuming the robot's hand becomes empty after placing the object
        box.in_bin_objects.append(obj)  # Add the object to the box's list of in-bin objects

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0.is_rigid = True, object0.is_compressible = False, object0.is_foldable = False
    # object1.is_foldable = True, object1.is_compressible = False, object1.is_rigid = False
    # object2.is_bendable = True, object2.is_compressible = False, object2.is_rigid = False
    # object3.is_compressible = True, object3.is_rigid = False, object3.is_foldable = False
    # object4.is_rigid = True, object4.is_compressible = False, object4.is_foldable = False

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order based on rules:
    # 1. Bend object2 (if bendable) before placing.
    # 2. Fold object1 (if foldable) before placing.
    # 3. Place object3 (compressible) and then push it.
    # 4. Place object0 and object4 (rigid) without constraints.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Bend object2
    action.bend(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    # Fold object1
    action.fold(object1, box)
    action.pick(object1, box)
    action.place(object1, box)

    # Place and push object3
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)

    # Place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Place object4
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by bending and folding objects before placing them.
    # Compressible objects are pushed after being placed.
    # Rigid objects are placed without additional actions.
    # Plastic objects are not bent, folded, or pushed, adhering to the rules.

    # Finally, add this code    
    print("All task planning is done")
