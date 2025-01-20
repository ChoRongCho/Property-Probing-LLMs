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
        if obj.object_type == "obj" and not obj.in_bin and self.robot_handempty:
            print(f"pick {obj.name}")
            self.state_holding(obj)
            # Update the box's in_bin_objects list if necessary
            if obj in box.in_bin_objects:
                box.in_bin_objects.remove(obj)
        else:
            print(f"Cannot pick {obj.name}")

    def place(self, obj, box):
        # Action Description: Place an object into the box. This action can be applied to any type of object.
        
        # Check if the object is plastic and if the constraint is applicable
        if obj.object_type == "plastic" and hasattr(obj, 'compressible'):
            # Check if there is a compressible object already in the box
            if any(o.object_type == "compressible" for o in box.in_bin_objects):
                print(f"place {obj.name}")
                self.state_handempty()  # Assuming the robot hand becomes empty after placing
                box.in_bin_objects.append(obj)
            else:
                print(f"Cannot place {obj.name}")
        else:
            # If the object is non-plastic or the constraint is not applicable, place it
            print(f"place {obj.name}")
            self.state_handempty()  # Assuming the robot hand becomes empty after placing
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
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', in_bin=False)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', in_bin=False)
object4 = Object(index=4, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', in_bin=False)
box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    # Assuming additional properties for demonstration purposes
    # object0: is_rigid=True, is_foldable=False, is_compressible=False, object_type='obj'
    # object1: is_rigid=True, is_foldable=False, is_compressible=True, object_type='obj'
    # object2: is_rigid=True, is_foldable=False, is_compressible=True, object_type='obj'
    # object3: is_rigid=True, is_foldable=True, is_compressible=False, object_type='obj'
    # object4: is_rigid=True, is_foldable=False, is_compressible=False, object_type='obj'
    
    # Rewrite the goal states of all objects given in the table in the following format.
    # object0: in_bin: True
    # object1: in_bin: True
    # object2: in_bin: True
    # object3: in_bin: True
    # object4: in_bin: True

    # Second, write a bin_packing order based on the given rules and the goal states of the objects.
    # 1. Fold object3 (if foldable)
    # 2. Pick object3
    # 3. Place object3
    # 4. Pick object1 (compressible)
    # 5. Place object1
    # 6. Push object1
    # 7. Pick object2 (compressible)
    # 8. Place object2
    # 9. Push object2
    # 10. Pick object0
    # 11. Place object0
    # 12. Pick object4
    # 13. Place object4

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(index=0, name='box', object_type='box', in_bin_objects=[])

    # b) Action sequence
    action.fold(object3, box)  # Fold object3 if foldable
    action.pick(object3, box)
    action.place(object3, box)
    
    action.pick(object1, box)
    action.place(object1, box)
    action.push(object1, box)  # Push object1 if compressible
    
    action.pick(object2, box)
    action.place(object2, box)
    action.push(object2, box)  # Push object2 if compressible
    
    action.pick(object0, box)
    action.place(object0, box)
    
    action.pick(object4, box)
    action.place(object4, box)

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    # The sequence follows the rules: fold foldable objects before picking, push compressible objects after placing,
    # and ensure no bending, folding, or pushing of plastic objects. Non-plastic objects are placed without constraints.

    # Finally, add this code    
    print("All task planning is done")
