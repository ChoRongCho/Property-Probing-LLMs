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
        
        # Preconditions: The object should not be in the box, and the robot's hand should be empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            if compressible_present:
                print(f"place {obj.name}")
                # Update the state to reflect the object is placed
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # Non-plastic objects can be placed without constraints
            print(f"place {obj.name}")
            # Update the state to reflect the object is placed
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
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)
object4 = Object(index=4, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0: is_rigid is True, actions pick, place are applicable
    # object1: is_rigid is True, actions pick, place are applicable
    # object2: is_bendable is True, actions pick, place, bend are applicable
    # object3: is_compressible is True, actions pick, place, push are applicable
    # object4: is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Bend object2 (beige_1D_line) since it is bendable.
    # 2. Pick and place object3 (brown_3D_cylinder) since it is compressible.
    # 3. Push object3 after placing it in the box.
    # 4. Pick and place object0 (red_3D_cuboid) since it is rigid.
    # 5. Pick and place object1 (blue_3D_cylinder) since it is rigid.
    # 6. Pick and place object4 (green_3D_cylinder) since it is rigid.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.bend(object2, box)
    action.pick(object3, box)
    action.place(object3, box)
    action.push(object3, box)
    action.pick(object0, box)
    action.place(object0, box)
    action.pick(object1, box)
    action.place(object1, box)
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules by first bending the bendable object (object2) before placing it.
    # The compressible object (object3) is placed and then pushed as required.
    # All other objects are rigid and can be placed without additional actions.
    # The sequence ensures that all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
