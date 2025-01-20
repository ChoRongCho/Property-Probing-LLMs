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
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Preconditions: The object is not in the box, and the robot's hand is empty.
        if not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is a plastic object and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_present = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            # If the constraint is not met, do not place the object
            if not compressible_present:
                print(f"Cannot place {obj.name}")
                return
        
        # If constraints are not applicable or are met, proceed to place the object
        print(f"place {obj.name}")
        
        # Update the state to reflect the object is now in the box
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
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False)
object2 = Object(index=2, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes
    # object0: is_rigid=True, actions pick, place are applicable
    # object1: is_rigid=True, actions pick, place are applicable
    # object2: is_foldable=True, actions pick, place, fold are applicable
    # object3: is_rigid=True, actions pick, place are applicable
    # object4: is_rigid=True, actions pick, place are applicable
    # object5: is_compressible=True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object2 (foldable) before placing.
    # 2. Pick and place object2.
    # 3. Pick and place object5 (compressible), then push.
    # 4. Pick and place object0.
    # 5. Pick and place object1.
    # 6. Pick and place object3.
    # 7. Pick and place object4.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)  # Fold object2
    action.pick(object2, box)  # Pick object2
    action.place(object2, box) # Place object2

    action.pick(object5, box)  # Pick object5
    action.place(object5, box) # Place object5
    action.push(object5, box)  # Push object5

    action.pick(object0, box)  # Pick object0
    action.place(object0, box) # Place object0

    action.pick(object1, box)  # Pick object1
    action.place(object1, box) # Place object1

    action.pick(object3, box)  # Pick object3
    action.place(object3, box) # Place object3

    action.pick(object4, box)  # Pick object4
    action.place(object4, box) # Place object4

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence respects all rules: foldable objects are folded before placing, compressible objects are pushed after placing,
    # and non-plastic objects are placed without constraints. The sequence ensures all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
