from scripts.utils.utils import int_to_ordinal


class PromptSet:
    def __init__(self, task, constraints, definition, primitives: dict):
        self.task = task
        self.constraints = constraints
        self.definition = definition
        self.primitives = primitives

        self.def_shape = "".join(self.definition["shape"])
        self.def_property = "".join(self.definition["properties"])
        self.def_dimension = "".join(self.definition["dimension"])

    def load_spatial_relationships(self):
        system_message = f"You are a vision AI designed to describe the spatial relationships of the objects. "
        message = """ 
The first image shows a top view of an object (the one which is the closest to the center of the image) while the second image shows a side view of them.
Each view captures the same scene, with the objects in the images corresponding one-to-one between the two views.
I will provide you with images that have bounding boxes drawn around the objects and its logits. 
However, unfortunately, these images can occasionally contain errors. 
Therefore, you need to make accurate judgments about the objects' positions and relationships. 
Additionally, the white lines represent the relationships between the bounding boxes, so think of this as a graph.

Based on the spatial information from this graph, you should be able to recognize the same objects. 
Please describe the given environment based on these images.      

Your answer must use the template below:

Please answer with the template below:
---template start---
### Objects and Their Descriptions:
# top view
|  top index  | descriptions  
|      1      |  
|      2      |
  
# side view
|  side index  | descriptions
|       1      |  
|       2      |

# Find same objects in both views 


### Spatial Relationships:

### Critical bounding box errors Description:
# if there is any critical error such as wrong bonding box and additional bounding box, describe here 

---template end---

  
"""

        return system_message, message

    def load_naming_message(self):
        # Use 1D, 2D, 3D definition of ChatGPT

        system_message = f"You are a vision AI designed to describe the shape and color of objects for {self.task}. " + \
                         "Analyze the given images of the objects and accurately describe their size and color. " + \
                         "Use the provided classification table to categorize the objects, " + \
                         "adhering strictly to the given classifications rather than relying on common sense."

        prompt = f"""
Now that you've obtained the spatial information of the objects, you need to describe shape, color, and dimension of each object.
And for clarity, I will provide the original images. Please identify the shape, dimension, and color of each object based on these images according to the definitions in "[Definitions of dimensions and shapes]" below.
Your answer must follow the naming convention which is "color_dimension_shape" (e.g., red_3D_cuboid or black_2D_ring).
Ensure that there is no contradiction between the shape and dimension. For example, "1D" and "loop" or "3D" and "circle" are not compatible according to their definitions in "[Definitions of dimensions and shapes]".

[Definitions of dimensions and shapes]
Dimension
{self.def_dimension}

Shape
{self.def_shape}

Your answer must use the template below:

Please answer with the template below:
---template start---
Answer
---
object: red_3D_polyhedron, yellow_3D_cuboid, ... # if there are duplicate objects, add '_N' at the end, e.g., red_3D_cuboid_2.
---

Descriptions about objects in the scene
*your descriptions in 200 words
---template end---
"""
        return system_message, prompt

    def load_prompt_object_class(self, object_dict: dict, max_predicates):
        system_message = f"""
You are an AI assistant responsible for converting the properties of objects into predicates.
Predicates for object properties will be assigned Boolean values. Please follow these rules:
1. Do not create more predicates than the given max_predicates.
2. Use the template provided below.
"""
        prompt = "Our goal is to define the types of objects and their predicates within the dataclass Object. \n"
        prompt += ("Here, we have the types, names, and properties of the objects recognized from the input images. "
                   "We need to use this information to complete the Object class. \n")
        for i, values in zip(list(object_dict.keys()), list(object_dict.values())):
            obj_name = values["name"]
            obj_pred = values["predicates"]
            prompt += f"{i}: name='{obj_name}', predicates={obj_pred}\n"
        prompt += f"""from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # physical state of an object
    in_bin: bool
    
    # Object physical properties 
    
    # pre-conditions and effects for {self.task} task planning (max: {max_predicates})
"""
        prompt += "However, we cannot complete a planning with this dataclass predicate alone" + \
                  f" which means that we have to add other predicates that fully describe {self.task} task. \n"

        return system_message, prompt

    def load_prompt_robot_action_prev(self, object_class_python_script):
        system_message = f"You are a good assistant"
        prompt = ("Our goal is to define the pre-conditions and effects for the robot's actions, "
                  "similar to how they are done in PDDL. \n")

        prompt += f"""
{object_class_python_script}\n\n
"""
        prompt += "This is an object class we should refer. \n"
        prompt += "What is the given predicates in this code? \n"
        prompt += "1. \n2. \n3. \n..."

        return system_message, prompt

    def load_prompt_robot_action(self,
                                 object_class_python_script):

        system_message = f"""_"""

        prompt = ("Now you have to make precondtions and effect of actions based on class Object and given predicates."
                  "Please refer to them to create actions. \n")

        prompt += f"""
class Robot:
    def __init__(self, name: str = "UR5"):
        self.name = name    
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True
    
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
    
    def pick(self, obj, bin):
        # make a pre-conditions for actions using if-else phrase
        # Action Description: {self.primitives["pick"]}
        print(f"Pick obj.name")
        print(f"Cannot Pick obj.name")
        
    def place(self, obj, bin):
        # Action Description: {self.primitives["place"]}
        print(f"Place obj.name in bin.name")
        print(f"Cannot Place obj.name")
        bin.in_bin_objects.append(obj)
    
    def bend(self, obj, bin):
        # Action Description: {self.primitives["bend"]}
        print(f"Fold obj.name")
        print(f"Cannot Fold obj.name")
        
    def fold(self, obj, bin):
        # Action Description: {self.primitives["fold"]}
        print(f"Fold obj.name")
        print(f"Cannot Fold obj.name")
        
    def push(self, obj, bin):
        # Action Description: {self.primitives["push"]}
        print(f"Push obj.name")
        print(f"Cannot Push obj.name")
        
    def out(self, obj, bin):
        # Action Description: {self.primitives["out"]}
        print(f"Out obj.name from bin.name")
        print(f"Cannot Out obj.name")
        bin.in_bin_objects.remove(obj)
        \n\n"""

        prompt += "Additionally, you must satisfy the following constraints. \n"
        for i, rule in enumerate(list(self.constraints.values())):
            prompt += f"{i + 1}: {rule}\n"

        prompt += "Please make more action preconditions and effect of the robot "
        prompt += f"For example, if a robot places an object in hand, obj.in_bin=False. \n"
        prompt += "However, if there are predicates that are mentioned in the constraints but not in the class Object, " + \
                  "do not reflect those constraints in preconditions. \n"
        prompt += """
Please answer with the template below:
---template start---
Answer:
```python
# only write a code here without example instantiation
class Robot:
    def __init__(self, ...):
        ...    
    def state_handempty(self):
        ...
    def state_holding(self, objects):
        ...  
    def state_base(self):
        ...
```
---template end---
"""
        return system_message, prompt

    def load_prompt_init_state(self,
                               object_dict,
                               object_python):

        system_message = ("You are going to organize the given content in a table. "
                          "These tasks are for defining initial states. ") + \
                         "Also, you should follow the template below. "

        prompt = f"We are now making initial state of the {self.task}. We get these information from the input images. \n\n"
        prompt += f"{object_dict}\n"
        prompt += f"{object_python}\n\n"

        prompt += "Using the above information, Please organize the initial state of the domain in a table. \n\n"
        prompt += """
Please answer with the template below:
---template start---
### 1. Init Table
# fill your table using objects predicates

### 2. Python Codes
# make init state into python code
# don't include the object classes or robot class, make only objects and bin 
# example  
```python
object0 = Object(index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', ...)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', ...)
box = Box()
```
...

### 3. Notes:
# Fill your notes
---template end---
"""

        return system_message, prompt

    def load_prompt_goal_state(self, init_state_table, goals, rules):
        system_message = "You are going to organize the given content in a table. These tasks are for defining a goal state. " + \
                         "Also, you should follow the template below. "

        prompt = (f"We are now making goal state of the {self.task}. "
                  f"Your goal is to redefine the goal state given in natural language into a table. \n\n")
        prompt += f"This is an init state table. \n"
        prompt += f"{init_state_table}\n\n"
        prompt += f"Our goal is listed below. \n"
        prompt += f"{goals}\n"
        prompt += f"And, this is rules that when you do actions. \n"
        prompt += f"{rules}\n\n"

        prompt += "\nUsing the above information, Please organize the goal state of the domain in a table. \n\n"
        prompt += """
Please answer with the template below:
---template start---
### 1. Goal Table
# fill your table similar with initial state

### 2. Notes:
# Fill your notes
---template end---
"""

        return system_message, prompt

    def load_prompt_planning_prev(self,
                                  object_class_python_script: str,
                                  robot_class_python_script: str,
                                  init_state_python_script: str,
                                  goal_state_table: str):
        system_message = f"You are a good assistant"
        prompt = "Refer this code. \n\n"
        prompt += f"{object_class_python_script}\n\n"
        prompt += f"{robot_class_python_script}\n\n"
        prompt += f"{init_state_python_script}\n\n"
        prompt += f"And this is the goal state table of all objects you should reach. \n{goal_state_table}\n\n"
        prompt += "Analyze actions and an initial state in 300 words"

        return system_message, prompt

    def load_prompt_planning(self):

        system_message = f"_"
        prompt = "Before start, you must follow the rules: \n"
        for i, rule in enumerate(list(self.constraints.values())):
            prompt += f"{i + 1}: {rule}\n"

        prompt += "Also, we remind the robot actions: \n"
        for pri, pri_def in zip(list(self.primitives.keys()), list(self.primitives.values())):
            prompt += f"{pri}: {pri_def}\n"

        prompt += f"""


Please answer with the template below:
---template start---

if __name__ == "__main__":
    # From initial state, remind object's key properties and available actions
    # object1: is_rigid -> pick, place, out
    # object2: is_foldable -> pick, place, fold, out 
    # object3: is_compressible -> pick, place, push, out
    # ...
    # And rewrite goal states of all objects
    # object1: in_bin: True
    # object2: in_bin: False 
    # object3: in_bin: True
    
    # Second, using given rules and object's states, make a task planning strategy
    # !!!Note: You can do folding action only if robot hand is empty
    
    # Third, make an action sequence.
    # a) Initialize the robot and the box
    robot = Robot() 
    box = Box(...)
    
    # b) Action sequence
    
    # Fourth, after making all actions, fill your reasons according to the rules
    ...
    
    # Finally, add this code    
    print("All task planning is done")
     
---template end---
"""

        return system_message, prompt

    def load_prompt_action_feedback(self, python_script, planning_output, rules, goals):
        system_message = ("You are a developer who catches and fixes errors in Python code. "
                          "You need to find the wrongs in the given code and its results and correct them. "
                          "Also, you should follow the template below. ")

        prompt = f"""This is a python code that you have to fix.\n
{python_script}\n\n 
This code consists of four parts below.
1. Object Class (Start with [@dataclass])
2. Robot Class (Start with [class Robot:])
3. Planning State (Start with [if __name__ == "__main__":])

And this is a result of the code.
{planning_output}

Here are rules and goals you should refer
rules: {rules}
goals: {goals}

All you need to do is fix the wrong action or syntax error in the given code. You have to use the goal state given in the code.
Please answer with the template below:

---template start---
# First, check the actions of robot class
a) Do pre-conditions satisfy the given rules?
b) Is the effect of action right?
c) Is there any syntax error in action codes?

# Second, check the symbolic robot action under [if __name__ == "__main__"]
d) Is the goal state right at assert part?
e) Is the order of robot action right?
f) Are there unnecessary actions?

Here, I'll give you a template.

# Wrong Part (Choose one from an error description) 
1. Object Class / 2. Robot Class / 3. Planning State

# Analysis using given error
# a) 
# b)
# c)
# d)
# e) 
# f)

# Modified Code (Make the error part only)
```python
# part 2 (example)

```
---template end---

"""

        return system_message, prompt

    def load_prompt_planner_feedback(self, python_script, planning_output, task_instruction, robot_action):
        prompt = f"We made a plan for a {self.task} and our goal is {self.constraints}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a old_result. \n"
        prompt += planning_output + " \n"

        prompt += "There are some planning errors in this code that is represented as Cannot. \n" + \
                  " Here are some rules for planning. \n"
        prompt += f"{task_instruction}\n"
        prompt += f"{robot_action}\n"

        prompt += "Please re-planning under the if __name__ == '__main__' part. \n"

        return prompt

    def load_verification_message(self, available_actions: list[bool], object_name):
        n = 2
        system_message = f"You're working to verify the object's properties through images for {self.task}." + \
                         f"This table defines the physical properties of the object we are investigating." + \
                         f"{self.def_property}" + \
                         f"Answer the questions below in accordance with this criterion. Also, you should follow the template below. "

        prompt = f"\nThe first two images are original images of {object_name}. Please refer to this image and answer. \n"
        end_message = f"""Please answer with the template below:  
---template start---
Answer  # If there is no mention of the object's properties, fill it with False. 
**rigid: True or False
**soft: True or False
**foldable: True or False
**elastic: True or False

Reason:
-Describe a object and feel free to write down your reasons for each properties in less than 50 words
---template end---
"""
        if available_actions[0]:  # push
            m1 = "We will show the image when the robot does the action 'push' on the object to verify the object is soft or rigid." + \
                 f"\nThe {int_to_ordinal(n + 1)} image is just before the robot pushes the object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image is the image when the robot is pushing the object. \n" + \
                 f"If there is a significant deformation in the shape of the object(see image {n + 1} and {n + 2}), the object is soft(3D), else it is rigid. " + \
                 f"Does this object have soft(only in 3D objects) or rigid properties? \n\n"
            n += 2
            prompt += m1

        if available_actions[1]:  # fold
            m2 = "We will show the image when the robot does the action 'fold' on the object to verify the object is foldable or elastic." + \
                 f"\nThe {int_to_ordinal(n + 1)} image shows the robot just before it grabs an object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image is after it is completely folded. \n" + \
                 f"The {int_to_ordinal(n + 3)} image shows after the robot leaves it hand on the object. \n" + \
                 f"If the end of the robot gripper that holds the object touches on the opposite side of the object(see image {n + 1} and {n + 2}), the object is not rigid. \n" + \
                 f"If the object return to its original shape after the robot lets go of the object(see image {n + 1} and {n + 3}), the object is elastic, else it is foldable. \n" + \
                 f"Does this object have foldable or elastic or None properties? \n\n"
            n += 3
            prompt += m2
        if available_actions[2]:  # pull
            m3 = "We will show the image when the robot does the action 'pull' on the object to verify the object is elastic or not." + \
                 f"\nThe {int_to_ordinal(n + 1)} image shows before the robot pulls an unknown object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image shows while the robot pulls the object. " + \
                 f"The {int_to_ordinal(n + 3)} image shows after the robot pulls the object. " + \
                 (f"If the object changes in size more than twice (see image {n + 1} and {n + 2}),"
                  f" and come back to its original shape(see image {n + 1} and {n + 3}), it is said to be elastic.") + \
                 f"Does this object have elastic properties? \n"
            n += 3
            prompt += m3
        prompt += end_message
        return system_message, prompt

    def load_property_probing_message_1(self):
        system_message = "You are good assistant. Don't make assumptions; just tell it like it is."
        prompt = "Describe about the object centered in the scene\n1. \n2. \n3. "

        return system_message, prompt

    def load_property_probing_message_2(self, object_name: str, action: str, property_keys: dict, before_pos=False):

        # property select code
        positive = list(property_keys[action].keys())[0]
        if action != "recover":
            negative = list(property_keys["None"].keys())[0]

        else:
            positive = before_pos
            negative = list(property_keys["recover"].keys())[0]

        prompt = (f"We will now probe the physical properties of objects bia "
                  f"the interaction between the manipulator and the objects.")

        prompt += f"We will now probe the object's properties. \n"
        prompt += f"""This defines the physical properties of object we are investigating.
{self.def_property}
 
In our case, we want to investigate about {positive} and {negative}. Are you ready?
"""

        return prompt

    def load_property_probing_message_3(self, object_name: str, action: str, property_keys: dict,
                                        before_pos=False) -> str:
        prompt = f"The images are images of {object_name}. Please refer to this image and answer.\n"

        # property select code
        positive = list(property_keys[action].keys())[0]
        if action != "recover":
            negative = list(property_keys["None"].keys())[0]

        else:
            positive = before_pos
            negative = list(property_keys["recover"].keys())[0]

        n = 0
        prompt += (
            f"We will show you the image when the robot does the action {action} on the object to verify the object is whether {positive} or {negative}"
            f"\nThe {int_to_ordinal(n + 1)} image is just before the robot {action} the object. \n"
            f"The {int_to_ordinal(n + 2)} image is the image when the robot is {action} the object. \n"
            f"If the object's shape has changed in the image, consider that '{positive}' occurred during {action} action."
            f"Does this object have '{positive}' or '{negative}' properties? \n\n")

        prompt += """
---template start---
1. Description of 1st image:
    - 
    
2. Description of 2st image:
    - 
    
3. Reasoning
    -  
    
4. Result
    - Property: ''

---template end---
"""
        return prompt

    def load_property_recover_message(self, object_name: str, action: str, property_keys: dict,
                                      before_action=False) -> str:
        prompt = f"The images are images of {object_name}. Please refer to this image and answer.\n"

        # property select code
        if action == "recover":
            positive = list(property_keys[before_action].keys())[0]
            negative = list(property_keys["recover"].keys())[0]
        else:
            raise ValueError

        n = 0
        prompt += (
            f"We will show you the image when the robot does the action {action} on the object to verify the object is whether {positive} or {negative}"
            f"\nThe {int_to_ordinal(n + 1)} image is just before the robot {before_action} the object. \n"
            f"The {int_to_ordinal(n + 2)} image is the image when the robot is {before_action} the object. \n"
            f"The {int_to_ordinal(n + 3)} image is the image after the robot is {action} the object. \n"
            f"If the object's shape recovers from deformation in the image, consider that '{positive}' occurred during {action}."
            f"Does this object have '{positive}' or '{negative}' properties? \n\n")

        prompt += """
---template start---
1. Description of 1st image:
    - 

2. Description of 2st image:
    - 

3. Reasoning
    - 

4. Result
    - Property: ''

---template end---
"""
        return prompt

    def load_prompt_vanilla_probing(self, obj_name=False, info=False):
        system_message = "You are good assistant"
        prompt = f"We will now probe the object's properties. \n"
        prompt += f"""This table defines the physical properties of the object we are investigating.
{self.def_property}
        
!Note1: we do not examine precise physical property of object but for {self.task}. This mean, when we investigate the properties of an object, we refer to its irreversibility rather than its physical feasibility
What is the property of the object? (choose only one property)
---template start---
1. Reasoning
    -  
    
2. Result
    - Property: ''

---template end---

Keep the template!!!
"""
        if obj_name:
            prompt = f"We will now probe the object's properties. \n"
            prompt += f"""This table defines the physical properties of the object we are investigating.
{self.def_property}

!Note1: we do not examine precise physical property of object but for {self.task}. This mean, when we investigate the properties of an object, we refer to its irreversibility rather than its physical feasibility

object name: {obj_name}
info
{info}

With these prior knowledge of the object, determine the property of the object. (choose only one property)
---template start---
1. Reasoning
    -  

2. Result
    - Property: ''

---template end---
"""
        return system_message, prompt

    def load_prompt_vanilla_three_image(self, obj_name, action: str):
        system_message = "You are good assistant"
        prompt = f"We will now probe the object's properties. \n"
        prompt += f"""This table defines the physical properties of the object we are investigating.
{self.def_property}

!Note1: we do not examine precise physical property of object but for {self.task}. This mean, when we investigate the properties of an object, we refer to its irreversibility rather than its physical feasibility

object name: {obj_name}
info
We will show you the three images when the robot does the action {action} on the object.
The first image is just before the robot {action} the object.
The second image is the image when the robot {action} the object.
The last image is the image after the robot recovers the object.

With these prior knowledge of the object, determine the property of the object. (choose only one property)
---template start---
1. Reasoning
    -  

2. Result
    - Property: ''

---template end---
"""
        return system_message, prompt
