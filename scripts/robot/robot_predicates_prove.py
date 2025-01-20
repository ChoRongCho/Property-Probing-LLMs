import os

from scripts.robot.robot import Robot
from scripts.utils.utils import list_file, sort_files


class RobotProve(Robot):
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None,
                 gpt_interface: object = False):
        super().__init__(name, goal, actions)

        self.predicates = self.active_predicates_list
        self.gpt_interface = gpt_interface

        self.action_1d = "bend"
        self.action_2d = "fold"
        self.action_3d = "push"
        self.action_recover = "recover"

        self.property_keys = {
            "bend": {"is_bendable": False},
            "fold": {"is_foldable": False},
            "push": {"is_compressible": False},
            "recover": {"is_plastic": False},
            "None": {"is_rigid": False},
        }

        self.data_path = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/predicates_prove"

    def reset_update_keys(self):
        self.property_keys = {
            "bend": {"is_bendable": False},
            "fold": {"is_foldable": False},
            "push": {"is_compressible": False},
            "recover": {"is_plastic": False},
            "None": {"is_rigid": False},
        }

    def get_object_predicates(self, database: dict, info: dict) -> list:
        target_name: str = info['name']
        name_list = list(database.keys())

        if target_name in name_list:
            predicates = database[target_name]["properties"]
            return predicates
        else:
            # random mode
            predicates = self.identifying_properties(target_name)

            predicates = ["is_rigid"]
            print(f"Can't find {target_name} in database. 'is_rigid' predicates are assigned. ")
            return predicates

    def gpt_prove_object(self, info, images):
        name = list(info.keys())[0]
        root = os.path.join(self.data_path, name)
        obj_data_path = list_file(root)
        obj_data_path = sort_files(obj_data_path)

    def get_datapath(self, name):
        pass

    def identifying_properties(self, target_name):
        # do probe space
        self.go_to_examine_space(target_name)

        # do probe
        if "1D" in target_name:
            is_bendable, is_rigid = self.probing_action(self.action_1d)
            if is_bendable:
                is_bendable, is_plastic = self.probing_action(self.action_recover)
                if is_bendable:
                    predicates = ["is_bendable"]
                else:
                    predicates = ["is_plastic"]
            else:
                predicates = ["is_rigid"]

        elif "2D" in target_name:
            is_foldable, is_rigid = self.probing_action(self.action_2d)
            if is_foldable:
                is_foldable, is_plastic = self.probing_action(self.action_recover)
                if is_foldable:
                    predicates = ["is_foldable"]
                else:
                    predicates = ["is_plastic"]
            else:
                predicates = ["is_rigid"]

        elif "3D" in target_name:
            is_compressible, is_rigid = self.probing_action(self.action_3d)
            if is_compressible:
                is_compressible, is_plastic = self.probing_action(self.action_recover)
                if is_compressible:
                    predicates = ["is_compressible"]
                else:
                    predicates = ["is_plastic"]
            else:
                predicates = ["is_rigid"]

        else:
            raise ValueError

        return predicates

    def go_to_examine_space(self, target_name):
        print(f"Move {target_name}")

    # def probing_action(self, action, images=None):
    #     """
    #
    #     self.update_keys = {
    #         "bend": {"is_bendable": False},
    #         "fold": {"is_foldable": False},
    #         "push": {"is_compressible": False},
    #         "recover": {"is_plastic": False},
    #         "None": {"is_rigid": False},
    #     }
    #
    #     :param action:
    #     :param images:
    #     :return:
    #     """
    #     if images is None:
    #         pass
    #
    #     # robot.do_action
    #     else:
    #         positive_property = self.property_keys[action]
    #         negative_property = self.property_keys["None"]
    #
    #     return True, False
