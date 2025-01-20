# from scripts.pddl_planner import PDDLPlanner
import os.path
import time

from scripts.utils.example import OBJS, PROPERTIES
# from scripts.python_planner import PythonPlanner
from scripts.python_planner import PythonPlanner
from scripts.utils.utils import parse_args_v2, save2csv_v2, initialize_csv_file

REPLANNING_INDEX = [1, 3, 6, 9, 10, 13, 17, 18, 20, 23, 24, 26, 29, 37]


def main_v2():
    args = parse_args_v2()
    inst_num = 38
    total_iter = 10
    planner = PythonPlanner(args=args)
    # start
    for iter_num in range(24141001, 24141001 + total_iter):
        planner.exp_number = str(iter_num)
        for i in range(1, inst_num + 1):
            if i in REPLANNING_INDEX:
                print(f"\nStart a number {i} experiment")
                planner.exp_name = f"instance{i}"
                planner.initiating_dir()
                planner.pseudo_plan(inst_num=i)


def probing_test():
    args = parse_args_v2()

    for i in range(1):
        args.exp_number = i + 1
        args.exp_name = 101
        planner = PythonPlanner(args=args)

        source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{i + 1}"
        obj_name = OBJS[i]
        images = [
            [os.path.join(source, "base_side.jpg")],
            [os.path.join(source, "probe_side.jpg")],
            [os.path.join(source, "recover_side.jpg")]
        ]
        properties = planner.probing_property(obj_name, images)
        gt = PROPERTIES[i]
        if properties == gt:
            print(f"Object{i + 1} has True predicates {properties}. ")
        else:
            print(f"Object{i + 1} has False predicates {properties} /// True: {gt}.  ")


def probing_exp():
    total_obj = 13
    total_iter = 10
    mode0_acc_list = []
    mode1_acc_list = []
    mode2_acc_list = []
    mode3_acc_list = []

    args = parse_args_v2()

    for obj_idx in range(2, 2 + total_obj):
        for mode in range(3, 4):
            obj_count = 0
            for iteration in range(total_iter):
                time.sleep(10)
                args.exp_number = obj_idx
                args.exp_name = 107 + mode + iteration * 1000
                planner = PythonPlanner(args=args)
                obj_name = OBJS[obj_idx - 1]
                if mode == 0:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [os.path.join(source, "base_side.jpg")]

                elif mode == 1:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [os.path.join(source, "base_side.jpg")]

                elif mode == 2:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [
                        [os.path.join(source, "base_side.jpg")],
                        [os.path.join(source, "probe_side.jpg")],
                        [os.path.join(source, "recover_side.jpg")]
                    ]

                elif mode == 3:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [
                        [os.path.join(source, "base_side.jpg")],
                        [os.path.join(source, "probe_side.jpg")],
                        [os.path.join(source, "recover_side.jpg")]
                    ]
                else:
                    raise ValueError

                properties = planner.property_probing_exp(obj_name=obj_name, images=images, mode=mode)
                gt = PROPERTIES[obj_idx - 1]
                if properties == gt:
                    obj_count += 1
                    print(f"EXP: {args.exp_number}-{args.exp_name}, Object{obj_idx} has True predicates {properties}. ")
                else:
                    print(
                        f"EXP: {args.exp_number}-{args.exp_name}, Object{obj_idx} has False predicates {properties}  /// True: {gt}.  ")

            if mode == 0:
                mode0_acc_list.append(obj_count / total_iter)
            elif mode == 1:
                mode1_acc_list.append(obj_count / total_iter)
            elif mode == 2:
                mode2_acc_list.append(obj_count / total_iter)
            elif mode == 3:
                mode3_acc_list.append(obj_count / total_iter)
    print("vanilla", mode0_acc_list)
    print("vanilla+CL", mode1_acc_list)
    print("vanilla inter", mode2_acc_list)
    print("Ours", mode3_acc_list)


def detect_objects_only():
    args = parse_args_v2()
    inst_num = 38
    total_iter = 10

    save_path = "/results/property_probing"
    planner = PythonPlanner(args=args)
    planner.image_version = 3

    # start
    for iter_num in range(24140001, 24140001 + total_iter):
        planner.exp_number = str(iter_num)
        result_csv_path = os.path.join(save_path, f"exp{iter_num}_results.csv")
        initialize_csv_file(result_csv_path)

        for i in range(1, inst_num + 1):
            print(f"\nStart a detection instance: {i}")
            planner.exp_name = f"instance{i}"

            """set"""
            planner.initiating_dir()
            planner.result_dir = os.path.join(save_path, f"instance{i}")
            planner.image_version = 3

            object_dict = planner.only_detection()
            save2csv_v2(instance=i, object_dict=object_dict, filename=result_csv_path)
            time.sleep(0.4)


def make_tracking_goal_state():
    args = parse_args_v2()
    positive = 0
    negative = 0
    negative_list = []

    inst_num = 38
    total_iter = 10
    replanning_num = 5
    planner = PythonPlanner(args=args)
    ture_num = 0
    for i in range(1, inst_num + 1):
        for iter_num in range(24141001, 24141001 + total_iter):
            planner.exp_number = str(iter_num)
            planner.exp_name = f"instance{i}"
            planner.initiating_dir()
            is_true = planner.make_tracking_goal_state(replanning_num=replanning_num)
            ture_num += is_true
    print(f"Replanning {replanning_num}: {ture_num}")
    # Replanning 0: 380 / 296 / goal vi 7
    # Replanning 1: 84 / 56 / 1
    # Replanning 2: 28 / 17 / 0
    # Replanning 3: 11 / 4 / 0
    # Replanning 4: 7 / 2 / 0
    # Replanning 5: 5 / 5 / 0


def plan_result():
    args = parse_args_v2()
    positive = 0
    negative = 0
    error = 0
    negative_list = []
    error_list = []

    inst_num = 38
    total_iter = 10
    replanning_num = 0
    planner = PythonPlanner(args=args)

    for i in range(1, inst_num + 1):
        print(f"---------------- Instance: {i} ----------------")
        for iter_num in range(250000, 250000 + total_iter):
            planner.exp_number = str(iter_num)
            planner.exp_name = f"instance{i}"
            planner.initiating_dir()
            planning_output, is_error = planner.run()
            # planning_output, is_error = planner.last_run()
            # planning_output, is_error = planner.tracking_goal_state(replanning_num=replanning_num)
            if is_error:
                error += 1
                error_list.append(f"exp{iter_num}, instance:{i}")
            else:
                if "Cannot" in planning_output:
                    negative += 1
                    negative_list.append(f"exp{iter_num}, instance:{i}")
                else:
                    positive += 1
                    if i in REPLANNING_INDEX:
                        print(f"Iter num : {iter_num}")
                        print(planning_output)
                        print("\n\n")
        print("-"*50)
        print(f"Inst{i}: Positive:{positive}, Negative: {negative}, Error: {error}, Total: {positive + negative}")

    print(f"Positive Rate: {round(positive / (positive + negative + error) * 100, 4)}%")
    print(f"Negative Rate: {round(negative / (positive + negative + error) * 100, 4)}%")
    print(f"Error Rate: {round(error / (positive + negative + error) * 100, 4)}%")
    print("-" * 50)
    for ne in negative_list:
        print("Negative: ", ne)
    print("-" * 50)
    for err in error_list:
        print("Error: ", err)
    print("-" * 50)


def replanning():

    args = parse_args_v2()
    inst_num = 38
    total_iter = 10
    planner = PythonPlanner(args=args)
    # start
    for iter_num in range(24141001, 24141001 + total_iter):
        planner.exp_number = str(iter_num)
        for i in range(1, inst_num + 1):
            if i in REPLANNING_INDEX:
                print(f"\n\nexp: {iter_num}, instance: {i}")
                planner.exp_name = f"instance{i}"
                planner.initiating_dir()
                planner.replanning()
                time.sleep(1)


def planning_without_prop():
    args = parse_args_v2()
    inst_num = 38
    total_iter = 10
    planner = PythonPlanner(args=args)
    for inst in range(32, 1+inst_num):
        for iter_num in range(300000, 300000 + total_iter):
            planner.exp_number = str(iter_num)
            planner.exp_name = f"instance{inst}"
            planner.initiating_dir()
            planner.no_prop_plan(inst)
            time.sleep(3)


if __name__ == '__main__':
    # detect_objects_only()
    # main_v2()
    print("\n---Start validating---\n")
    # plan_result()
    # make_tracking_goal_state()
    # replanning()
    # tracking_goal_state()
    planning_without_prop()

    print("Done")
