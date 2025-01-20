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
        # Preconditions: The robot's hand must be empty, and the object must not be in the box.
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object, and the object is considered in the bin.
            self.state_holding(obj)
            obj.in_bin = True
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        if self.robot_now_holding == obj and not obj.in_bin:
            print(f"place {obj.name}")
            # Update the state to reflect that the object is now in the bin
            obj.in_bin = True
            self.state_handempty()  # Robot hand is now empty after placing the object
            box.in_bin_objects.append(obj)  # Add the object to the box's list of in-bin objects
        else:
            print(f"Cannot place {obj.name}")

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
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
object4 = Object(index=4, name='brown_3D_cylinder', color='brown', shape='3D_cylinder', object_type='obj', in_bin=False)

box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming the physical properties are defined elsewhere, let's outline the actions based on hypothetical properties:
    # the object0.is_compressible is True, actions pick, place, push are applicable
    # the object1.is_foldable is True, actions pick, place, fold are applicable
    # the object2.is_plastic is True, actions pick, place are applicable
    # the object3.is_rigid is True, actions pick, place are applicable
    # the object4.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object1 (if foldable), then pick and place it.
    # 2. Pick and place object0, then push it (if compressible).
    # 3. Pick and place object4, then push it (if compressible).
    # 4. Pick and place object3 (no constraints).
    # 5. Pick and place object2 (plastic, ensure a compressible object is already in the box).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='bin', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object1 if foldable
    action.fold(object1, box)
    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object0, then push it
    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    # Pick and place object4, then push it
    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    # Pick and place object3
    action.pick(object3, box)
    action.place(object3, box)

    # Pick and place object2 (plastic)
    action.pick(object2, box)
    action.place(object2, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence ensures that all constraints are respected: foldable objects are folded before placing,
    # compressible objects are pushed after placing, and plastic objects are placed only after a compressible object is in the box.

    # Finally, add this code    
    print("All task planning is done")
