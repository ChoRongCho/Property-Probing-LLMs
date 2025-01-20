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
        if obj.object_type == "obj" and not obj.in_bin:
            print(f"pick {obj.name}")
            # State the effect of Action: the robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            # If the constraint is satisfied or not applicable, place the object
            if compressible_in_box:
                print(f"place {obj.name}")
                # Update the state to reflect the object is placed
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name} due to constraint")
        else:
            # For non-plastic objects, place without constraints
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
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object1 = Object(index=1, name='beige_1D_line', color='beige', shape='1D_line', object_type='obj', in_bin=False)
object2 = Object(index=2, name='black_1D_line', color='black', shape='1D_line', object_type='obj', in_bin=False)
object3 = Object(index=3, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes:
    # object0: is_foldable = True, actions pick, place, fold are applicable
    # object1: is_rigid = True, actions pick, place are applicable
    # object2: is_rigid = True, actions pick, place are applicable
    # object3: is_compressible = True, actions pick, place, push are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object0 (if applicable)
    # 2. Pick object0
    # 3. Place object0
    # 4. Pick object3
    # 5. Place object3
    # 6. Push object3
    # 7. Pick object1
    # 8. Place object1
    # 9. Pick object2
    # 10. Place object2

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object0, box)  # Fold object0 if applicable
    action.pick(object0, box)  # Pick object0
    action.place(object0, box)  # Place object0
    action.pick(object3, box)  # Pick object3
    action.place(object3, box)  # Place object3
    action.push(object3, box)  # Push object3
    action.pick(object1, box)  # Pick object1
    action.place(object1, box)  # Place object1
    action.pick(object2, box)  # Pick object2
    action.place(object2, box)  # Place object2

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: 
    # - Object0 is foldable, so it is folded before picking and placing.
    # - Object3 is compressible, so it is pushed after placing.
    # - Objects1 and 2 are rigid, so they are simply picked and placed without additional actions.
    # - The sequence ensures that all objects are placed in the box as per the goal states.

    # Finally, add this code    
    print("All task planning is done")
