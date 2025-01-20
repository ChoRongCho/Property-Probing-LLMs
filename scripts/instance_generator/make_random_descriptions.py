import json
import os
import random
import pandas as pd

base_goal_list = [
    "packing all objects into the bin",
    "Packing all items into the box.",
    "Storing all objects in the container.",
    "Fitting all belongings into the bin",
]
goal_list = [
    "If there is a black object, don't pack it into the box",
    "If there is a elastic object, don't pack it into the box",
    "If there is a yellow object, don't pack it into the box",
    "If there is a rigid object, don't pack it into the box",
    "If there is a 1D object, don't pack it into the box",
    "If there is a red object, don't pack it into the box",
    "If there is a white and soft object, don't pack it into the box",
    "If there are foldable object and soft object together, don't pack a foldable object into the box",
    "If there are yellow object and black object together, don't pack a black object into the box",
    "If there is a fragile object, don't pack it into the box",
]

base_rule = [
    "you should never pick and place a box",
    "don't pick and place a box called bin",
    "it is prohibited to lift and relocate a container",
    "avoid handling and moving any box",
    "never attempt to pick up and set down an object named box",
]
rule_list = [
    "when fold a object, the object must be foldable",
    "when place a rigid objects in the bin, the soft objects must be in the bin before",
    "when fold a foldable object, the fragile object must be in the bin ",
]
sim_rule1 = [
    "do not place a fragile object if there is no elastic object in the bin",
    "when place a fragile objects, the soft objects must be in the bin",
]
sim_rule2 = [
    "if a rigid object in the bin at the initial state, pick out of the rigid object and replace it into the bin ",
    "if a soft object in the bin at the initial state, pick out of the soft object and replace it into the bin ",
]
sim_rule3 = [
    "when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted",
    "you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object",
    "when push a object, neither fragile and rigid objects are permitted"
]


def select_goals(base_goal_list, goal_list):
    goals = {}
    goals["1"] = random.choice(base_goal_list)

    num_additional_goals = random.choices([0, 1, 2], weights=[0.2, 0.5, 0.3], k=1)[0]
    additional_goals = random.sample(goal_list, num_additional_goals)

    for i, goal in enumerate(additional_goals, start=2):
        goals[str(i)] = goal

    return goals


def select_rules(base_rule, rule_list, sim_rule1, sim_rule2, sim_rule3):
    while True:
        rules = {}
        rules["1"] = random.choice(base_rule)

        num_rule_list = random.randint(1, 2)
        selected_rule_list = random.sample(rule_list, num_rule_list)

        num_sim_rule1 = random.randint(0, 1)
        selected_sim_rule1 = random.sample(sim_rule1, num_sim_rule1)

        num_sim_rule2 = random.randint(0, 1)
        selected_sim_rule2 = random.sample(sim_rule2, num_sim_rule2)

        num_sim_rule3 = random.randint(0, 1)
        selected_sim_rule3 = random.sample(sim_rule3, num_sim_rule3)

        all_selected_rules = selected_rule_list + selected_sim_rule1 + selected_sim_rule2 + selected_sim_rule3

        if 2 <= len(all_selected_rules) <= 3:  # Minimum 2 additional rules plus the base rule makes 3
            for i, rule in enumerate(all_selected_rules, start=2):
                rules[str(i)] = rule

            return rules


def main():
    root_folder = '/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning'
    total_json = {}

    # Creating folders and saving JSON files.
    for i in range(1, 37):
        folder_name = f"instance{i}"
        folder_path = os.path.join(root_folder, folder_name)

        data = {
            "bin_packing": {
                "task_description": "packing objects into the box called bin. ",
                "goals": select_goals(base_goal_list, goal_list),
                "rules": select_rules(base_rule, rule_list, sim_rule1, sim_rule2, sim_rule3)
            }
        }
        total_json[folder_name] = {
            "goal": data["bin_packing"]["goals"],
            "rule": data["bin_packing"]["rules"]
        }

        # make folder
        os.makedirs(folder_path, exist_ok=True)

        # JSON file path
        json_file_path = os.path.join(folder_path, "instructions.json")

        # Save JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"'instructions.json' is saved successfully in Folder '{folder_name}'")

    total_json_file_path = os.path.join(root_folder, "total_instructions.json")
    with open(total_json_file_path, 'w') as total_json_file:
        json.dump(total_json, total_json_file, indent=4)
    print("All JSON files saved successfully.")


def rename_folder(src_folder, new_folder_name):
    parent_dir = os.path.dirname(src_folder)
    new_folder_path = os.path.join(parent_dir, new_folder_name)

    os.rename(src_folder, new_folder_path)
    print(f"Renamed folder: {src_folder} to {new_folder_path}")


def generate_random_numbers(n):
    data = []

    # 각 숫자 개수에 대한 확률 분포 (3, 4, 5, 6개)
    num_count_options = [3, 4, 5, 6]
    probabilities = [0.1, 0.25, 0.35, 0.3]

    unique_combinations = set()

    for i in range(1, n + 1):
        while True:
            num_count = random.choices(num_count_options, probabilities)[0]  # 확률에 따른 숫자 개수 선택
            random_numbers = sorted(random.sample(range(1, 15), num_count))  # 중복 없이 랜덤 뽑기
            if tuple(random_numbers) not in unique_combinations:  # 중복 체크
                unique_combinations.add(tuple(random_numbers))
                row = [i] + random_numbers  # instance 번호와 뽑힌 숫자들
                data.append(row)
                break
            else:
                data.append([i])  # 중복된 경우 instance 번호만 추가

    return data


if __name__ == '__main__':
    instance = generate_random_numbers(40)
    df = pd.DataFrame(instance)
    df.to_csv('/home/changmin/PycharmProjects/OPTPlan/random_numbers.csv', index=False)
    print(df)


