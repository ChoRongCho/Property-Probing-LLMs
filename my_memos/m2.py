from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates

    # bin_packing predicates expressed as a boolean (max 3)
    is_in_box: bool = False
    is_out_box: bool = True


class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions

        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False

    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False

    # basic state
    def state_base(self):
        self.robot_base_pose = True

    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_out_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")

    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")

    def push(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_in_box and obj.is_soft:
            # Effects
            print(f"Push {obj.name}")

    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")

    def pick_out(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")
            self.state_handempty()

    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True,
                 is_out_box=True, is_in_box=False)
object1 = Object(index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True,
                 is_out_box=True, is_in_box=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True,
                 is_out_box=True, is_in_box=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_rigid=True,
                 is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_in_box=True,
                 is_out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> is_in_box: True, is_out_box: False
    # object1 (white_1D_ring) -> is_in_box: True, is_out_box: False
    # object2 (blue_1D_ring) -> is_in_box: False, is_out_box: True
    # object3 (white_2D_circle) -> is_in_box: True, is_out_box: False
    # object4 (white_box) -> is_in_box: True, is_out_box: False (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Never pick and place a box
    # Rule 3: When placing soft objects, the soft objects must be pushed before packed in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, take it out and replace it into the bin

    # Step 1: Pick out the rigid object (white_2D_circle) and place it back
    robot.pick_out(object3, bin)
    robot.place(object3, bin)

    # Step 2: Pick and push the soft object (yellow_3D_cuboid) before placing it in the bin
    robot.pick(object0, bin)
    robot.push(object0, bin)
    robot.place(object0, bin)

    # Step 3: Pick and place the elastic object (white_1D_ring) in the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == False
    assert object3.is_in_box == True
    assert object4.is_in_box == True
    print("All task planning is done")


