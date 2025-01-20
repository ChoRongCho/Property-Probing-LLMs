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
        
        # Preconditions: The object must not be in the box, and the robot's hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint should be applied
        if hasattr(obj, 'material') and obj.material == 'plastic':
            # Check if there's a compressible object already in the box
            compressible_in_box = any(
                hasattr(o, 'material') and o.material == 'compressible' for o in box.in_bin_objects
            )
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return
        
        # Place the object in the box
        box.in_bin_objects.append(obj)
        self.state_handempty()
        print(f"place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Example assumptions for demonstration:
    # object0: is_rigid=True, actions pick, place are applicable
    # object1: is_compressible=True, actions pick, place, push are applicable
    # object2: is_foldable=True, actions pick, place, fold are applicable
    # object3: is_bendable=True, actions pick, place, bend are applicable
    # object4: is_rigid=True, actions pick, place are applicable
    # object5: is_plastic=True, actions pick, place are applicable (requires compressible in box first)

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: 
    # 1. Fold object2 (foldable), then pick and place it.
    # 2. Bend object3 (bendable), then pick and place it.
    # 3. Pick and place object1 (compressible), then push it.
    # 4. Pick and place object0 (rigid).
    # 5. Pick and place object4 (rigid).
    # 6. Pick and place object5 (plastic, requires compressible in box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)
    
    action.bend(object3, box)
    action.pick(object3, box)
    action.place(object3, box)
    
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)
    
    action.pick(object0, box)
    action.place(object0, box)
    
    action.pick(object4, box)
    action.place(object4, box)
    
    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are done before picking, compressible objects are pushed after placing, and the plastic object is placed only after a compressible object is in the box.

    # Finally, add this code    
    print("All task planning is done")
