import os
import re
import subprocess

from scripts.planner import PlannerFramework
from scripts.utils.example import DICT_LIST


class PythonPlanner(PlannerFramework):
    def __init__(self, args):
        super().__init__(args=args)
        self.args = args

    def plan_and_run(self):
        self.plan()
        self.run()

    def plan(self):
        self.make_plan()

    def no_prop_plan(self, inst_num: int):
        task_data = self.task_data
        task_data["goals"] = "Pack all the objects."
        self.planning_naive()

    def pseudo_plan(self, inst_num: int):
        """
        test with random goal and constraints and without visual detection
        only for task planning

        :return: planning code
        """
        task_data = self.task_data
        # task_data["goals"] = GOALS[inst_num - 1]
        task_data["goals"] = "Pack all the objects."
        self.make_pseudo_plan(DICT_LIST[inst_num - 1])

    def run(self):
        file_path = os.path.join(self.result_dir, "planning.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"There is no file at {file_path}. ")
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')
            is_error = True
        else:
            planning_output = output.decode('utf-8') + "\n"
            is_error = False
        if self.is_save:
            file_path = os.path.join(self.result_dir, "planning_first_run_result.txt")
            with open(file_path, "w") as file:
                file.write(str(planning_output) + "\n\n")
                file.close()
        return planning_output, is_error

    def last_run(self):
        # file_path = os.path.join(self.result_dir, "planning.py")
        files = os.listdir(self.result_dir)
        python_files = [f for f in files if f.endswith('.py')]
        numbered_files = []
        for file in python_files:
            match = re.search(r'(\d+)', file)  # 파일 이름에서 숫자 검색
            if match:
                numbered_files.append((file, int(match.group(1))))  # (파일 이름, 숫자)로 저장

        numbered_files.sort(key=lambda x: x[1], reverse=True)
        if numbered_files:
            file_path = os.path.join(self.result_dir, numbered_files[0][0])
        else:
            file_path = os.path.join(self.result_dir, "planning.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"There is no file at {file_path}. ")
        # print(file_path)
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')
            is_error = True
        else:
            planning_output = output.decode('utf-8') + "\n"
            is_error = False
        return planning_output, is_error

    def replanning(self):
        for i in range(self.max_replanning):
            is_feed = self.planning_feedback()
            if "Success" in is_feed:
                print(is_feed)
                break
            else:
                print(is_feed)
                pass

    def make_tracking_goal_state(self, replanning_num=0):
        # file_path = os.path.join(self.result_dir, "planning.py")
        if replanning_num == 0:
            file_path = os.path.join(self.result_dir, "planning.py")
            new_file_path = os.path.join(self.result_dir, "planning_goal_track.py")
        else:
            file_path = os.path.join(self.result_dir, f"planning_feed{replanning_num}.py")
            new_file_path = os.path.join(self.result_dir, f"planning_feed{replanning_num}_goal_track.py")

        if not os.path.exists(file_path):
            return 0

        with open(file_path, "r") as file:
            content = file.read()
            file.close()

        sections = self.separate_code_block(python_code=content)
        initial_state = sections["initial_state_python"]
        object_names = re.findall(r'^(object\d+)\s*=', initial_state, flags=re.MULTILINE)
        output_string = f"\n    all_objects = [{', '.join(object_names)}]\n"
        output_string += "    for an_obj in all_objects:\n"
        output_string += f"        print('Name:', an_obj.name, ' || In bin:', an_obj.in_bin)\n"

        new_content = content + output_string
        # print(new_file_path)
        if new_file_path:
            with open(new_file_path, "w") as file:
                file.write(new_content)
                file.close()

        return 1

    def tracking_goal_state(self, replanning_num=0):
        if replanning_num == 0:
            file_path = os.path.join(self.result_dir, "planning_goal_track.py")
        else:
            file_path = os.path.join(self.result_dir, f"planning_feed{replanning_num}_goal_track.py")

        if not os.path.exists(file_path):
            return "0", "0"

        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')
            is_error = True
        else:
            planning_output = output.decode('utf-8') + "\n"
            is_error = False
        return planning_output, is_error

