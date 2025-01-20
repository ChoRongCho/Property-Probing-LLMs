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
    is_rigid: bool = False
    is_compressible: bool = False
    is_plastic: bool = False

    # Additional predicates for bin_packing (max: 1)
    is_3D: bool = False


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
        # Preconditions: The robot's hand must be empty, and the object must not be in the bin.
        if self.robot_handempty and not obj.in_bin:
            # Action Description: Pick an object that is not in the box. The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effects: The robot is now holding the object, and the hand is no longer empty.
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note: If a predicate required by the constraints is absent from the class Object, do not consider the constraints.

        # Check if the object is plastic and if the box already contains a compressible object
        if obj.is_plastic:
            has_compressible = any(o.is_compressible for o in box.in_bin_objects)
            if not has_compressible:
                print(f"Cannot place {obj.name}")
                return

        # Preconditions: The robot must be holding the object and the object must not already be in a bin
        if self.robot_now_holding == obj and not obj.in_bin:
            # Effects: Place the object in the box and update the states
            box.in_bin_objects.append(obj)
            obj.in_bin = True
            self.state_handempty()
            print(f"place {obj.name}")
        else:
            print(f"Cannot place {obj.name}")

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and is 3D
        if obj.is_compressible and obj.is_3D:
            # Preconditions: The robot's hand must be empty before pushing
            if self.robot_handempty:
                print(f"push {obj.name}")
                # Effects: The robot's hand remains empty after pushing
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name}: Hand is not empty")
        else:
            print(f"Cannot push {obj.name}: Object is not compressible and 3D")

    def fold(self, obj, box):
        print('Cannot fold')

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)
object1 = Object(index=1, name='gray_1D_line', color='gray', shape='1D_line', object_type='obj', in_bin=False, is_plastic=True)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_3D=True)
object3 = Object(index=3, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_rigid=True, is_3D=True)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_rigid is True and object0.is_3D is True, actions pick, place are applicable
    # object1.is_plastic is True, actions pick, place are applicable (with constraints)
    # object2.is_compressible is True and object2.is_3D is True, actions pick, place, push are applicable
    # object3.is_rigid is True and object3.is_3D is True, actions pick, place are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Pick and place object2 (compressible) into the box, then push it.
    # 2. Pick and place object1 (plastic) into the box, since object2 (compressible) is already in the box.
    # 3. Pick and place object0 (rigid) into the box.
    # 4. Pick and place object3 (rigid) into the box.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name="box1", object_type="box", in_bin_objects=[])

    # b) Action sequence
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)
    
    action.pick(object1, box)
    action.place(object1, box)
    
    action.pick(object0, box)
    action.place(object0, box)
    
    action.pick(object3, box)
    action.place(object3, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence starts by placing the compressible object (object2) into the box and pushing it, 
    # which satisfies the rule that a compressible object should be pushed after placing.
    # Then, the plastic object (object1) is placed, as the rule requires a compressible object to be in the box first.
    # Finally, the rigid objects (object0 and object3) are placed without any additional constraints.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
