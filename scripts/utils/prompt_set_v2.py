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

        self.basic_robot_states = """
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
"""
        self.basic_object_class = """from dataclasses import dataclass


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
"""

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

    def load_prompt_object_class(self, object_dict, max_predicates):
        system_message = f"""You are an AI assistant responsible for converting the properties of objects into predicates used in generating an action sequence for {self.task}. The predicates for object properties will be assigned Boolean values. Please follow these rules:
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

    # physical state of an object for {self.task}
    in_bin: bool

    # Object physical properties 
    
    # Additional predicates for bin_packing (max: {max_predicates})

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
        prompt += "This is the object class we should reference. \n"
        prompt += "What are the `# Object physical properties` we need to consider? Please provide an answer in 100 words. \n"
        prompt += "1. \n2. \n3. \n..."

        return system_message, prompt

    def load_prompt_robot_action_primitives(self, primitive: str, object_class_ps):
        system_message = ""
        prompt = "This is Object class you have to use. \n\n"
        prompt += object_class_ps

        prompt += ("\nDefine the preconditions and effects of actions based on the `Object` class. "
                   "Use these to create actions. \n")

        for i, rule in enumerate(list(self.constraints.values())):
            if primitive in rule.lower():
                if i == 0:
                    prompt += "Additionally, ensure the following constraints are satisfied: \n"
                prompt += f"Constraint{i + 1}: {rule}\n"

        prompt += "\n"
        prompt += ("However, if any of the objects are not with the physical property mentioned in this constraints, ignore this constraints."
                   f"ignore the constraint and do not reflect it in `def {primitive}(self, obj, bin):`. "
                   f"Generate the function 'print('{primitive}', obj.name)' without making any assumptions. \n")

        prompt += f"""
{self.basic_robot_states}

Answer:
```python
    # only write a `def {primitive}` here without examples and `class Action`
    def {primitive}(self, obj, box):
        if ~~~~: 
        # Action Description: {self.primitives[primitive]}  
        # Note! If a predicate required by the constraints is absent from the class Object, do not consider the constraints.
            print(f"{primitive} obj.name")
            # state the effect of Action and box: self.state_holding or self.state_handempty etc if necessary
            ...effect...
            
        else:
            print(f"Cannot {primitive} obj.name")
```
"""
        return system_message, prompt

    def load_prompt_action_verif(self, primitive: str,
                                 action_class_pc: str,
                                 active_predicates: list,
                                 object_class_ps: str):
        system_message = "You are a good code writer"
        prompt = "This is Object class you have to use. \n\n"
        prompt += object_class_ps
        prompt = "And, this is the basic state of the action you have to use. \n\n"
        prompt += self.basic_robot_states

        prompt = "Finally, This is a part of the code within the Action class that you are going to revise. \n\n"
        prompt += f"{action_class_pc}\n\n"

        prompt += f"The set of objects has {len(active_predicates)} predicates: "
        if active_predicates:
            for index, predicate in enumerate(active_predicates):
                if predicate == active_predicates[-1]:
                    prompt += f"and {index+1}. {predicate}."
                else:
                    prompt += f"{index+1}. {predicate}, "
        else:
            prompt += "We don't have to consider physical properties of the object. \n"
        prompt += "\n"

        # Question Start~Q1
        prompt += f"Q1. Please write the expected output. \n"
        if active_predicates:
            for index, predicate in enumerate(active_predicates):
                prompt += f"{index+1}. Can {primitive} {predicate} object? \n"
        else:
            prompt += "\n"
        prompt += "\n"

        # Question Start~Q2
        prompt += "Q2. Verify that the code aligns with the definition and constraints: \n"
        prompt += f"Def: {self.primitives[primitive]}\n"
        for i, rule in enumerate(list(self.constraints.values())):
            if primitive in rule.lower():
                prompt += f"Constraint{i + 1}: {rule}\n"
        prompt += "\n"

        # Question Start~Q3
        prompt += (f"Q3. If there are errors in Q2, revise the '{primitive}' code only. "
                   f"Note! Do not add predicates that is not exist in the original code!"
                   f"If there is no error, just rewrite the code. \n\n")
        prompt += f"""
Answer:
```python
    def {primitive}(self, obj, bin):
        if the object meets the constraints and the action description:
            # Action Description: {self.primitives[primitive]}  
            # Note! if there is no predicates in Object but required for constraints, ignore the constraints!
            print(f"{primitive} obj.name")
            ...effect... # also check the effect that they obey the action description
        else:
            print(f"Cannot {primitive} obj.name")
```        
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

    def load_prompt_goal_state(self, object_dict, goals):
        system_message = ("We are going to organize the given content in a table. "
                          "These tasks are for defining a goal state. "
                          "Also, you should follow the template below. ")

        prompt = (f"We are currently defining the goal state for the {self.task}. "
                  f"Your task is to translate the goal state provided in natural language into a table. \n\n")
        prompt += f"This is a collection of target objects for the {self.task} task. \n"
        prompt += f"{object_dict}\n\n"
        prompt += f"Our goal is as follows: \n"
        prompt += f"{goals}\n"

        prompt += "\nUsing the information, please organize the goal state of the domain into a table. \n\n"
        prompt += """
Please answer with the template below:
---template start---
### 1. Goal Table
| Index | Name | State1 | State2 | ...
|-------|------|--------|--------|-----
|   0   |      |  True  |  False | ...
|   1   |      |  True  |  True  | ...
|   2   |      |  False |  False | ...
|  ...  |  ..  |   ..   |   ..   | ...

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
        prompt = ("Refer the following code containing the list of actions (class Action)"
                  " and the set of initial states of objects which are defined in class Object. \n\n")
        prompt += f"{object_class_python_script}\n\n"
        prompt += f"{robot_class_python_script}\n\n"
        prompt += f"{init_state_python_script}\n\n"
        prompt += f"And this is the table of goal states where all objects should reach. \n{goal_state_table}\n\n"
        prompt += ("Fully understand the actions in the Action class and the initial states of all objects. "
                   "Then tell me your understanding in 300 words.")

        return system_message, prompt

    def load_prompt_planning(self):
        system_message = f"_"
        prompt = "Before start, you must follow the rules: \n"
        for i, rule in enumerate(list(self.constraints.values())):
            prompt += f"{i+1}: {rule}\n"

        prompt += "\nAlso, we remind you the robot actions: \n"
        for pri, pri_def in zip(list(self.primitives.keys()), list(self.primitives.values())):
            prompt += f"{pri}: {pri_def}\n"

        prompt += f"""
        
Please answer with the template below:
---template start---

if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    <Example>
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_foldable is True, actions pick, place, fold are applicable
    # the object3.is_compressible is True, actions pick, place, push are applicable
    # ...
    
    <Example>
    # Rewrite the goal states of all objects given in the table in the following format.
    # object1: in_bin: True
    # object2: in_bin: False 
    # object3: in_bin: True
    # ...

    # Second, write a {self.task} order based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume or change the physical properties of the object.
    # Write here.


    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(...)

    # b) Action sequence
    

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    ...

    # Finally, add this code    
    print("All task planning is done")

---template end---
"""
        return system_message, prompt

    def load_prompt_planning_result(self, python_script, planning_output):
        """
        if error exist
        :param python_script:
        :param planning_output:
        :return:
        """
        system_message = ("You are a developer who catches and fixes errors in Python code. "
                          "You need to find the wrongs in the given code and its results and correct them. "
                          "Also, you should follow the template below. ")

        prompt = f"""This is a python code that you are going to fix.\n
{python_script}\n\n 
This code consists of four parts below.
1. Object Class (Start with [@dataclass])
2. Action Class (Start with [class Action:])
3. Object initial State (Start with [# Object Initial State])
4. Planning State (Start with [if __name__ == "__main__":])

And this is a planning result of the code.
{planning_output}
"""
        return system_message, prompt

    def load_prompt_syntax_target(self):
        system_message = ""
        prompt = """
Identify any incorrect parts and revise the faulty sections based on the provided planning results.

---template start---
### Wrong part (Select only one from the planning result.)
1. Object Class 
2. Action Class 
3. Object initial State 
4. Planning State 

### Reason (Tell me your understanding in 300 words.)

### Revised version (Revise the wrong part selected above.)
```python
# 2. Action Class (example)
```
---template end---
"""
        return system_message, prompt

    def load_prompt_action_feedback(self):
        system_message = ""
        prompt = f"""
Here are constraints you should refer.
rules: {self.constraints}

Your task is to identify any errors in the preconditions and effects of the action within the given Action class.
!!! One notable thing is that, in many cases, these actions may be error-free. 
Therefore, if no errors are detected, simply return it as is.

Please answer with the template below:
---template start---
First, analyze the error message.
1.
2.
3.

Second, check the error part follows the notes
!!Note1. Do not assume the physical properties of the object.
!!Note2. If a predicate required by the constraints is not defined in the class Object, ignore the constraints please. 
# For example, treating a rigid object as a compressible object. They are different.
# For example, treating a bendable object as a foldable object. They are different.

Third, find the error part of the class Action
# Example
# def place() part is wrong. In our objects set, there is no compressible object. 
# However, the precondtion in 'def place()' violates the Note2 because they make precondtions ~~~

---template end---
"""

        return system_message, prompt

    def load_prompt_revise_action(self,
                                  action_python_script):
        system_message = "_"
        prompt = ("Now you have to revise precondtions and effect of actions "
                  "based on class Object and given predicates. \n")
        prompt += f"""
{action_python_script}
"""
        prompt += "Additionally, you must satisfy the following constraints.\n"
        for i, rule in enumerate(list(self.constraints.values())):
            prompt += f"{i + 1}: {rule}\n"

        prompt += "Please revise pre-conditions and effect of the action "
        prompt += """
Please answer with the template below:
---template start---
Answer:
```python
# only write a code here without example instantiation
# Note! If a predicate required by the constraints is not defined in the class Object, ignore the constraints!!!
class Action:
    def __init__(self, ...):
        ...    
    def state_handempty(self):
        ...
    def state_holding(self, objects):
        ...  
    def state_base(self):
        ...
        ...
    def bend(self, obj, box): <-- Don't revise such part (We don't have to revise them)
        print('Cannot bend')
        ...
```
---template end---
"""
        return system_message, prompt

    def load_prompt_planner_feedback(self, python_script, planning_output, goals):
        system_message = "You are a good assistant"
        prompt = f"We made a plan for a {self.task} and our goal is '{goals}'. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + "\n\n"

        prompt += "And this is a result of the Python script. \n"
        prompt += planning_output + "\n\n"

        prompt += "Before start, you must follow the rules: \n"
        for i, rule in enumerate(list(self.constraints.values())):
            prompt += f"{i + 1}: {rule}\n"
        prompt += """
---template start---
First, analyze the planning strategy of the previous code.

Second, find the wrong part of the planning under <if __name__ == '__main__'> part
# What is wrong part? 
# 1. Order that does not meet the constraints  
# 2. Unnecessary actions  
# 3. Actions that do not align with the goal state  

Re-planning the code 
```python
if __name__ == "__main__":
    # First, from initial state, recall the physical properties of objects and available actions:
    <Example>
    # the object1.is_rigid is True, actions pick, place are applicable
    # the object2.is_foldable is True, actions pick, place, fold are applicable
    # the object3.is_compressible is True, actions pick, place, push are applicable
    # ...
    
    <Example>
    # Rewrite the goal states of all objects given in the table in the following format.
    # object1: in_bin: True
    # object2: in_bin: False 
    # object3: in_bin: True
    # ...

    # Second, write a plan strategy based on the given rules and the goal states of the objects.
    # !!Note1: Common Mistakes! pick -> fold -> place (x), fold -> pick -> place (o) 
    # !!Note2: Do not assume the physical properties of the object.
    # !!Note3: If a predicate required by the constraints is absent from the class Object, do not consider the constraints.

    # Third, make an action sequence.
    # a) Initialize the robot and the box
    action = Action() 
    box = Box(...)

    # b) Action sequence
    

    # Fourth, after making all actions, provide your reasoning based on the given rules.
    ...

    # Finally, add this code    
    print("All task planning is done")
```
---template end---
"""
        prompt += "Please replanning under the if __name__ == '__main__' part. \n"
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

    def load_property_recover_message(self,
                                      object_name: str,
                                      action: str,
                                      property_keys: dict,
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

    def top_down_planning(self, goals):

        system_message = f"You are a task planner for {self.task}"
        prompt = f"""
Goal of the {self.task}: {goals}
\nAvailable actions: 
"""
        for pri, pri_def in zip(list(self.primitives.keys()), list(self.primitives.values())):
            prompt += f"{pri}: {pri_def}\n"

        prompt += "\nConstraints: \n"
        for i, rule in enumerate(list(self.constraints.values())):
            prompt += f"{i+1}: {rule}\n"

        prompt += """

1. Describe the given images.
2. Create a plan that adheres to the given constraints and instructions.

---template start---
1. Description 
    - Describe the objects in the scene.
    - Identify the physical property of each object.
        [rigid, bendalbe, foldable, compressible, plastic(irreversibly deformable)]   
        1. 
        2.
        3.

2. Grounded Plan

 
---template end---
"""
        return system_message, prompt
