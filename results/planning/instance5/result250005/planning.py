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
        # Preconditions: The robot's hand must be empty and the object must not be in the box
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is a plastic object and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            # If a compressible object is present, or if the constraint does not apply, proceed
            if compressible_present or not hasattr(obj, 'object_type'):
                print(f"place {obj.name}")
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name} due to constraint")
        
        else:
            # For non-plastic objects, place without constraints
            print(f"place {obj.name}")
            self.state_handempty()
            box.in_bin_objects.append(obj)

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
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object2 = Object(index=2, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_rigid is True, actions pick, place are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_rigid is True, actions pick, place are applicable
    # the object3.is_rigid is True, actions pick, place are applicable
    # the object4.is_rigid is True, actions pick, place are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume or change the physical properties of the object.
    # Write here.
    # Since no objects are specified as plastic, compressible, bendable, or foldable, we assume all are rigid.
    # Therefore, the order can be straightforward: pick -> place for each object.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object0, box)
    action.place(object0, box)
    
    action.pick(object1, box)
    action.place(object1, box)
    
    action.pick(object2, box)
    action.place(object2, box)
    
    action.pick(object3, box)
    action.place(object3, box)
    
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # Since all objects are rigid and there are no specific constraints like plastic, compressible, bendable, or foldable,
    # the actions are straightforward. Each object is picked and placed into the box without any additional operations.
    # The robot's hand is empty before and after each pick and place action, adhering to the constraints.

    # Finally, add this code    
    print("All task planning is done")
