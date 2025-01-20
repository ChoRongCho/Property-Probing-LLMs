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
    is_foldable: bool

    # Additional predicates for bin_packing (max: 1)
    is_placed: bool


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
        # Preconditions: The object is not in the bin and the robot hand is empty
        if not obj.in_bin and self.robot_handempty:
            # Action Description: Pick an object that is not in the box. 
            # The action does not include the 'place' action and can be applied to any type of object.
            print(f"pick {obj.name}")
            # Effect: The robot is now holding the object
            self.state_holding(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Check if the object is already placed
        if obj.is_placed:
            print(f"Cannot place {obj.name}, it is already placed.")
            return

        # Check if the object is of type 'obj' and if constraints apply
        if obj.object_type == 'obj':
            # Check if the object is compressible or rigid or foldable
            if obj.is_compressible or obj.is_rigid or obj.is_foldable:
                # Check if the object is plastic and if a compressible object is already in the box
                if obj.color == 'plastic':
                    compressible_in_box = any(o.is_compressible for o in box.in_bin_objects)
                    if not compressible_in_box:
                        print(f"Cannot place {obj.name}, a compressible object must be in the box first.")
                        return

        # Action Description: Place an object into the box. This action can be applied to any type of object.
        print(f"place {obj.name}")
        # Update the state to reflect the object is now placed
        obj.is_placed = True
        # Add the object to the box
        box.in_bin_objects.append(obj)
        # Update the robot state
        self.state_handempty()

    def bend(self, obj, box):
        print('Cannot bend')

    def push(self, obj, box):
        # Check if the object is compressible and not made of plastic
        if obj.is_compressible and obj.object_type != "plastic":
            # Preconditions: The robot's hand must be empty
            if self.robot_handempty:
                # Action Description: Push a 3D compressible object downward in the bin
                print(f"push {obj.name}")
                # Effects: The robot's hand remains empty after pushing
                self.state_handempty()
            else:
                print(f"Cannot push {obj.name} because the robot is holding something")
        else:
            print(f"Cannot push {obj.name} due to constraints")

    def fold(self, obj, box):
        # Check if the object is foldable and not plastic
        if obj.is_foldable and obj.object_type != 'plastic':
            # Action Description: Fold a 2D foldable object. Hand must remain empty before and after the folding.
            print(f"fold {obj.name}")
            # Effects: Ensure the robot's hand is empty before and after folding
            self.state_handempty()
        else:
            print(f"Cannot fold {obj.name}")

    def dummy(self):
        pass
# Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_foldable=False, is_placed=False)
object1 = Object(index=1, name='blue_3D_cylinder', color='blue', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=False, is_rigid=True, is_foldable=False, is_placed=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_foldable=False, is_placed=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False, is_compressible=False, is_rigid=False, is_foldable=True, is_placed=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False, is_compressible=True, is_rigid=False, is_foldable=False, is_placed=False)

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # object0.is_compressible is True, actions pick, place, push are applicable
    # object1.is_rigid is True, actions pick, place are applicable
    # object2.is_compressible is True, actions pick, place, push are applicable
    # object3.is_foldable is True, actions pick, place, fold are applicable
    # object4.is_compressible is True, actions pick, place, push are applicable
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (yellow_2D_rectangle) because it is foldable.
    # 2. Pick and place object3 into the box.
    # 3. Pick and place object0 (yellow_3D_cuboid) because it is compressible.
    # 4. Push object0 in the box.
    # 5. Pick and place object2 (white_3D_cylinder) because it is compressible.
    # 6. Push object2 in the box.
    # 7. Pick and place object4 (red_3D_polyhedron) because it is compressible.
    # 8. Push object4 in the box.
    # 9. Pick and place object1 (blue_3D_cylinder) because it is rigid and non-plastic.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)
    action.pick(object3, box)
    action.place(object3, box)

    action.pick(object0, box)
    action.place(object0, box)
    action.push(object0, box)

    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)

    action.pick(object4, box)
    action.place(object4, box)
    action.push(object4, box)

    action.pick(object1, box)
    action.place(object1, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold the foldable object before placing it, place compressible objects first, and push them after placing. 
    # Non-plastic objects are placed without additional constraints. The sequence ensures all objects are packed according to their properties and the rules.

    # Finally, add this code    
    print("All task planning is done")

    all_objects = [object0, object1, object2, object3, object4]
    for an_obj in all_objects:
        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)
