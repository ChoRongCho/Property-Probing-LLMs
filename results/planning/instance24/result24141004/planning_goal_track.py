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
    is_plastic: bool
    is_foldable: bool

    # Additional predicates for bin_packing (max: 1)
    is_fragile: bool  # Additional predicate for handling delicate items


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
        # Preconditions: The object is not in the bin and the robot's hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is plastic and if the constraint applies
        if obj.is_plastic and hasattr(obj, 'is_compressible'):
            # Check if there is a compressible object already in the box
            compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
            if not compressible_in_box:
                print(f"Cannot place {obj.name}")
                return

        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        # Update the state to reflect the object is now in the box
        obj.in_bin = True
        box.in_bin_objects.append(obj)
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Action Description: Push a 3D compressible object downward in the bin. 
        # Hand must remain empty before and after the pushing.
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
        
        if self.robot_handempty and obj.in_bin and obj.is_compressible and not obj.is_plastic:
            print(f"push {obj.name}")
            # Since the hand must remain empty before and after the push, no state change is needed.
            self.state_handempty()
        else:
            print(f"Cannot push {obj.name}")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if hasattr(obj, 'is_foldable') and obj.is_foldable and hasattr(obj, 'is_plastic') and not obj.is_plastic:
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Assuming the robot's hand should remain empty before and after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_plastic=False, is_foldable=False, is_fragile=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_plastic=False, is_foldable=False, is_fragile=False)
object2 = Object(index=2, name='blue_2D_rectangle', color='blue', shape='2D_rectangle', object_type='obj', in_bin=False, is_compressible=False, is_rigid=False, is_plastic=True, is_foldable=False, is_fragile=False)
object3 = Object(index=3, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', in_bin=False, is_compressible=False, is_rigid=False, is_plastic=False, is_foldable=True, is_fragile=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_plastic=False, is_foldable=False, is_fragile=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_plastic=False, is_foldable=False, is_fragile=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # the object0.is_compressible is True, actions pick, place, push are applicable
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_plastic is True, actions pick, place are applicable (requires compressible object in box first)
    # the object3.is_foldable is True, actions pick, place, fold are applicable
    # the object4.is_compressible is True, actions pick, place, push are applicable
    # the object5.is_rigid is True, actions pick, place are applicable

    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True
    # object5: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (transparent_2D_circle) since it is foldable.
    # 2. Pick and place object3.
    # 3. Pick and place object0 (yellow_3D_cuboid) since it is compressible.
    # 4. Push object0.
    # 5. Pick and place object4 (red_3D_polyhedron) since it is compressible.
    # 6. Push object4.
    # 7. Pick and place object2 (blue_2D_rectangle) since a compressible object is already in the box.
    # 8. Pick and place object1 (blue_3D_cylinder).
    # 9. Pick and place object5 (green_3D_cylinder).

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box1', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object2, box)
    action.place(object2, box)

    action.pick(object1, box)
    action.place(object1, box)

    action.pick(object5, box)
    action.place(object5, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing, place compressible objects first,
    # and push them after placing. The plastic object is placed only after a compressible object is in the box.
    # Non-plastic, non-compressible objects are placed without additional constraints.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4, object5]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
