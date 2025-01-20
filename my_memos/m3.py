from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    location: tuple
    size: tuple
    color: str or bool
    object_type: str

    # Object physical properties predicates
    is_elastic: bool = False
    is_rigid: bool = False
    is_fragile: bool = False

    # bin_packing Predicates (max 5)
    in_bin: bool = False
    out_bin: bool = False
    is_stackable: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False


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
        self.robot_now_holding = False
        self.robot_base_pose = True

        # new state for bin_packing
        self.is_elastic_in_bin = False
        self.is_elastic_is_pushed = False

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False

    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False

    # basic state
    def state_base(self):
        self.robot_base_pose = True

    # bin_packing
    def pick(self, obj):
        if obj.in_bin or obj.object_type == 'box':
            print(f"Cannot pick a {obj.name} in the bin or a box.")
        else:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_bin = True
            obj.in_bin = False

    # bin_packing
    def place(self, obj, bins):
        if self.robot_now_holding != obj or obj.object_type == 'box':
            print(f"Cannot place a {obj.name} not in hand or a box.")
        elif bins:
            # place an object in the bin
            if not self.is_elastic_in_bin and obj.is_fragile:
                print(f"Cannot place a {obj.name} without the elastic object in the box. ")
            elif obj.is_soft:
                if self.is_elastic_is_pushed:
                    self.is_elastic_in_bin = True
                    print(f"Place {obj.name} in {bins.name}")
                    self.state_handempty()
                    obj.in_bin = True
                    obj.out_bin = False
                else:
                    print(f"Cannot place a {obj.name} before pushed. ")
            else:
                print(f"Place {obj.name} in {bins.name}")
                self.state_handempty()
                obj.in_bin = True
                obj.out_bin = False
        else:
            # place an object out of the bin
            print(f"Place {obj.name} out of the box")
            self.state_handempty()
            obj.in_bin = False
            obj.out_bin = True

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty or obj.is_fragile or obj.is_rigid:
            print(f"Cannot push a {obj.name} when hand is not empty or the object is fragile or rigid.")
        else:
            if obj.is_elastic:
                self.is_elastic_is_pushed = True
            print(f"Push {obj.name}")

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty:
            print(f"Cannot fold a {obj.name} when hand is not empty")
        else:
            print(f"There is no is_foldable object in the domain to fold")

    # bin_packing
    def out(self, obj, bins):
        if not obj.in_bin:
            print(f"Cannot pick a {obj.name} not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False
            obj.out_bin = True


# Bin
bin1 = Object(
    index=2,
    name='white box',
    location=(498, 218),
    size=(249, 353),
    color='white',
    object_type='bin',
    is_fragile=True,
    in_bin=True
)

# Object 1
object1 = Object(
    index=0,
    name='yellow object',
    location=(89, 136),
    size=(156, 154),
    color='yellow',
    object_type='object',
    is_elastic=True,
    out_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='blue object',
    location=(203, 278),
    size=(156, 150),
    color='blue',
    object_type='object',
    is_rigid=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=3,
    name='black object',
    location=(294, 150),
    size=(147, 123),
    color='black',
    object_type='object',
    is_fragile=True,
    out_bin=True,
)

# if __name__ == '__main__':
# 	# packing all object in the box
# 	# make a plan
#
# You must follow the rule:
#
# {'pick': 'pick an {object} not in the {bin}', 'place': 'place an {object} on the {anywhere}', 'push': 'push an {object} downward in the bin, hand must be empty when pushing', 'fold': 'fold an {object}, hand must be empty when folding. you can fold the object in_bin or out_bin', 'out': 'pick an {object} in {bin}'}
# rule0: "you should never pick and place a box",
# rule1: "before place a elastic object, push a elastic object "
# rule2: "do not place a fragile object if there is no elastic object in the bin",
# rule3: "when push a object, neither fragile and rigid are permitted"
# Make a plan under the if __name__ == '__main__': and reflect the rules that are not considered at the robot action part.
# You must make a correct order.


# ----------------------------------------------------------


if __name__ == '__main__':
    """
    bin
    fragile but we don't have to consider this predicates.

    rules
    rule0: "you should never pick and place a box",
    rule1: "before place a elastic object, push a elastic object "
    rule2: "do not place a fragile object if there is no elastic object in the bin",
    rule3: "when push a object, neither fragile and rigid are permitted"

    objects
    1 elastic objects: object1
    1 rigid object: object2
    1 fragile object: object3

    objects in the bin:
    objects out the bin: object1, object2, object3

    Available action
    object1: [elastic, out_bin]: pick, place, push
    object2: [rigid, out_bin]: pick, place
    object3: [fragile, out_bin]: pick, place
    """
    # Initialize robot
    robot = Robot()

    # Push, pick and place an elastic object1 based on rule1
    robot.push(object1)
    robot.pick(object1)
    robot.place(object1, bin1)

    # place fragile object3 in the bin based on the rule2
    robot.pick(object3)
    robot.place(object3, bin1)

    # Pick and place object2
    robot.pick(object2)
    robot.place(object2, bin1)

    # End the planning
    robot.state_base()
