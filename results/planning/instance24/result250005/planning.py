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
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Preconditions
        if self.robot_handempty and not obj.in_bin:
            print(f"pick {obj.name}")
            # Effect: Update the state to reflect that the robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        # Check if the object is plastic and if the constraint is applicable
        if obj.object_type == "plastic":
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.object_type == "compressible" for o in box.in_bin_objects)
            
            if compressible_in_box:
                print(f"place {obj.name}")
                # Update the state to reflect the object being placed
                self.state_handempty()
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # For non-plastic objects, place without constraints
            print(f"place {obj.name}")
            # Update the state to reflect the object being placed
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

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Note: Since the physical properties like is_rigid, is_foldable, etc., are not explicitly defined in the Object class,
    # we will assume them based on the object_type or shape for this example.
    
    # Example assumptions based on object_type or shape:
    # the object0 is rigid, actions pick, place are applicable
    # the object1 is rigid, actions pick, place are applicable
    # the object2 is foldable (2D shape), actions pick, place, fold are applicable
    # the object3 is foldable (2D shape), actions pick, place, fold are applicable
    # the object4 is rigid, actions pick, place are applicable
    # the object5 is compressible (3D shape), actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # Order: 
    # 1. Fold object2 (blue_2D_rectangle) before placing.
    # 2. Fold object3 (transparent_2D_circle) before placing.
    # 3. Pick and place object5 (green_3D_cylinder), then push it.
    # 4. Pick and place object0 (yellow_3D_cuboid).
    # 5. Pick and place object1 (blue_3D_cylinder).
    # 6. Pick and place object4 (red_3D_polyhedron).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object2, box)
    action.pick(object2, box)
    action.place(object2, box)

    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object5, box)
    action.place(object5, box)
    action.push(object5, box)

    action.pick(object0, box)
    action.place(object0, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: foldable objects are folded before placing, compressible objects are pushed after placing,
    # and non-plastic objects are placed without constraints. The sequence ensures that all objects are placed in the box
    # according to their physical properties and the given rules.

    # Finally, add this code    
    print("All task planning is done")
