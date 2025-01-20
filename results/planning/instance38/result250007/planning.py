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
        # Preconditions: The object is not in the box and the robot's hand is empty
        if obj not in box.in_bin_objects and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. 
            # The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # If constraints do not apply or are satisfied, proceed with placing the object
        print(f"place {obj.name}")
        # Update the state to reflect the object is no longer being held
        self.state_handempty()
        # Add the object to the box's list of in-bin objects
        box.in_bin_objects.append(obj)
        # Update the object's state to reflect it is now in the bin
        obj.in_bin = True

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object1 = Object(index=1, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0 is a 2D object, assume it is foldable, actions pick, place, fold are applicable
    # object1 is a 1D object, assume it is bendable, actions pick, place, bend are applicable
    # object2 is a 3D object, assume it is compressible, actions pick, place, push are applicable
    # object3 is a 3D object, assume it is rigid, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 (if applicable), then pick and place it.
    # 2. Bend object1 (if applicable), then pick and place it.
    # 3. Pick and place object2, then push it.
    # 4. Pick and place object3.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object0 if applicable
    action.fold(object0, box)
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)

    # Bend object1 if applicable
    action.bend(object1, box)
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)
    # Push object2
    action.push(object2, box)

    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are done before picking, 
    # and push is done after placing compressible objects. The constraints for plastic objects 
    # are not applicable here as none of the objects are plastic. The sequence ensures all objects 
    # are placed in the box as per the goal state.

    # Finally, add this code    
    print("All task planning is done")
