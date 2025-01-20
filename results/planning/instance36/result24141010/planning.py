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
    is_foldable: bool = False
    is_rigid: bool = False
    is_bendable: bool = False
    is_plastic: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_placed: bool = False


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
        # Preconditions: The object must not be in the bin, and the robot hand must be empty.
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is already placed
        if obj.is_placed:
            print(f"Cannot place {obj.name}, it is already placed.")
            return
        
        # Check if the robot is holding the object
        if not self.robot_now_holding == obj:
            print(f"Cannot place {obj.name}, it is not being held.")
            return
        
        # Check constraint: If the object is plastic, ensure a compressible object is already in the box
        if obj.is_plastic:
            compressible_present = any(o.is_foldable or o.is_bendable for o in box.in_bin_objects)
            if not compressible_present:
                print(f"Cannot place {obj.name}, no compressible object in the box.")
                return
        
        # Place the object in the box
        print(f"place {obj.name}")
        obj.is_placed = True
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        
        # Update the robot's state
        self.state_handempty()

    def bend(self, obj, box):
        # Check if the object is bendable and not plastic
        if obj.is_bendable and not obj.is_plastic:
            # Action Description: Bend a bendable object. Hand must remain empty before and after the bending action.
            if self.robot_handempty:
                print(f"bend {obj.name}")
                # No change in robot's state as hand remains empty
                self.state_handempty()
            else:
                print(f"Cannot bend {obj.name} because the hand is not empty")
        else:
            print(f"Cannot bend {obj.name} because it is not bendable or is plastic")

    def push(self, obj, box):
        print('Cannot push')

    def fold(self, obj, box):
        # Check if the object is foldable and the robot's hand is empty
        if obj.is_foldable and self.robot_handempty:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # No change in the robot's state since the hand remains empty
            # No effect on the box or object state is specified
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_foldable=True)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False, is_rigid=True)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False, is_bendable=True)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_foldable is True, actions pick, place, fold are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_bendable is True, actions pick, place, bend are applicable
    # object3.is_plastic is True, actions pick, place are applicable (with constraints)

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 (foldable) -> pick -> place -> push
    # 2. Bend object2 (bendable) -> pick -> place -> push
    # 3. Pick object1 (rigid) -> place
    # 4. Pick object3 (plastic) -> place (after a compressible object is in the box)

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action()
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    # Fold object0
    action.fold(object0, box)
    # Pick and place object0
    action.pick(object0, box)
    action.place(object0, box)
    # Push object0
    action.push(object0, box)

    # Bend object2
    action.bend(object2, box)
    # Pick and place object2
    action.pick(object2, box)
    action.place(object2, box)
    # Push object2
    action.push(object2, box)

    # Pick and place object1
    action.pick(object1, box)
    action.place(object1, box)

    # Pick and place object3 (plastic, after compressible objects are in the box)
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold and bend actions are performed before picking and placing.
    # Compressible objects (object0 and object2) are pushed after being placed.
    # The plastic object (object3) is placed only after a compressible object is in the box.

    # Finally, add this code    
    print("All task planning is done")
