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
    is_compressible: bool
    is_rigid: bool

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

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj

    def pick(self, obj, box):
        # Preconditions: The robot's hand must be empty, and the object must not already be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the bin.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Preconditions: The robot must be holding the object, and the object must not already be in the bin.
        if not self.robot_handempty and not obj.in_bin:
            # Check if the object is a box or obj
            if obj.object_type == "obj":
                # Check if the box already contains a compressible object if the object is plastic
                if obj.is_compressible or any(o.is_compressible for o in box.in_bin_objects):
                    # Effects: Place the object in the box.
                    print(f"place {obj.name}")
                    self.state_handempty()
                    obj.in_bin = True
                    box.in_bin_objects.append(obj)
                else:
                    print(f"Cannot place {obj.name} - requires a compressible object in the box first")
            else:
                # If the object is a box, place it without constraints
                print(f"place {obj.name}")
                self.state_handempty()
                obj.in_bin = True
                box.in_bin_objects.append(obj)
        else:
            print(f"Cannot place {obj.name} - preconditions not met")

    def push(self, obj, box):
        # Preconditions: The object must be compressible, the robot's hand must be empty, and the object must be in the bin.
        if obj.is_compressible and self.robot_handempty and obj.in_bin:
            # Action Description: Push a 3D compressible object downward in the bin.
            print(f"push {obj.name}")
            # Effects: The robot's hand remains empty after the push.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass

# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_3D=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_3D=True)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_3D=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_3D=True)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_compressible is True, actions pick, place, push are applicable
    # object2.is_rigid is True, actions pick, place are applicable
    # object3.is_compressible is True, actions pick, place, push are applicable
    # object4.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place a compressible object first to satisfy the rule for placing plastic objects.
    # 2. Push the compressible object after placing it.
    # 3. Place non-plastic objects without constraints.
    # 4. Ensure all objects are in the bin as per the goal state.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.pick(object0, box)  # Pick yellow_3D_cuboid
    action.place(object0, box)  # Place yellow_3D_cuboid
    action.push(object0, box)  # Push yellow_3D_cuboid

    action.pick(object1, box)  # Pick white_3D_cylinder
    action.place(object1, box)  # Place white_3D_cylinder
    action.push(object1, box)  # Push white_3D_cylinder

    action.pick(object3, box)  # Pick brown_3D_cylinder
    action.place(object3, box)  # Place brown_3D_cylinder
    action.push(object3, box)  # Push brown_3D_cylinder

    action.pick(object2, box)  # Pick beige_1D_line
    action.place(object2, box)  # Place beige_1D_line

    action.pick(object4, box)  # Pick green_3D_cylinder
    action.place(object4, box)  # Place green_3D_cylinder

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts by placing compressible objects first, which allows subsequent placement of any plastic objects.
    # Each compressible object is pushed after being placed, adhering to the rules.
    # Non-plastic objects are placed without additional constraints.
    # The sequence ensures all objects are in the bin, achieving the goal state.

    # Finally, add this code    
    print("All task planning is done")


    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
