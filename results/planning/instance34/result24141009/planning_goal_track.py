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
    is_bendable: bool

    # Additional predicates for bin_packing (max: 1)
    is_fragile: bool


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
            obj.in_bin = False  # Update the object's state to reflect it's being held, not in a bin.
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the robot is holding the object and the object is not already in a bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Check if the object is a box or obj and apply constraints if necessary
            if obj.object_type == "obj":
                # Check if the object is compressible (since the constraint mentions compressible objects)
                if obj.is_compressible or obj.object_type != "plastic":
                    print(f"place {obj.name}")
                    # Update the object's state to be in the bin
                    obj.in_bin = True
                    # Update the box's list of in-bin objects
                    box.in_bin_objects.append(obj)
                    # Update the robot's state to hand empty
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} due to constraints")
            else:
                # If the object is a box, place it without constraints
                print(f"place {obj.name}")
                obj.in_bin = True
                box.in_bin_objects.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is bendable
        if obj.is_bendable:
            print(f"bend {obj.name}")
            # Since the hand must remain empty before and after the bending action, ensure the robot's state reflects this
            self.state_handempty()
        else:
            print(f"Cannot bend {obj.name}")

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        if self.robot_handempty and obj.in_bin and obj.is_compressible:
            print(f"push {obj.name}")
            # No change in state as hand remains empty
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_fragile=False)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_compressible=False, is_bendable=True, is_fragile=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_bendable=False, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0 is compressible, actions pick, place, push are applicable
    # object1 is bendable, actions pick, place, bend are applicable
    # object2 is compressible, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object1 (black_1D_line) since it is bendable.
    # 2. Pick and place object0 (white_3D_cylinder) since it is compressible and can be placed without constraints.
    # 3. Push object0 after placing it in the box.
    # 4. Pick and place object1 (black_1D_line) after bending.
    # 5. Pick and place object2 (red_3D_polyhedron) since it is compressible.
    # 6. Push object2 after placing it in the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object1, box)  # Bend the bendable object
    action.pick(object0, box)  # Pick the compressible object
    action.place(object0, box) # Place the compressible object
    action.push(object0, box)  # Push the compressible object
    action.pick(object1, box)  # Pick the bendable object
    action.place(object1, box) # Place the bendable object
    action.pick(object2, box)  # Pick the compressible object
    action.place(object2, box) # Place the compressible object
    action.push(object2, box)  # Push the compressible object

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: bend the bendable object before placing, place compressible objects first, and push them after placing.
    # The actions are performed in a logical order to ensure all objects are packed according to their properties and constraints.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
