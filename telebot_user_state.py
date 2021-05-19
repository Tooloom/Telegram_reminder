"""Addition for PyTelegramApiBOT module user states and saves user input"""

# -*- coding: utf-8 -*-

import json
import os

USERSTATES_FILE = '.t_bot_users_data/users_state.json'
main_data_states = {
    "main_users_state": {}
}


def get_full_data_user_path(user_id: str):
    """Returns full path for save user data"""
    return ".t_bot_users_data/%s.telebot_data" % user_id


class UserStates():
    """Main user states class"""

    def __init__(self):
        """Inits users states and creates users states file"""
        if not os.path.exists('.t_bot_users_data'):
            os.mkdir('.t_bot_users_data')
        if not os.path.exists(USERSTATES_FILE):
            with open(USERSTATES_FILE, 'w+', encoding='utf-8') as states_file:
                json.dump(
                    main_data_states, states_file, indent=4, ensure_ascii=False
                )

    def update_state(self, user_id: int, user_state: str):
        """Updates user state"""
        user_id = str(user_id)
        with open(USERSTATES_FILE, 'r+', encoding='utf-8') as states_file:
            data_userstates = json.load(states_file)
            tmp_user_data = "{'%s': '%s'}" % (user_id, user_state)
            valid_json_str = tmp_user_data.replace("'", "\"")
            valid_json_str = json.loads(valid_json_str)
            data_userstates['main_users_state'].update(valid_json_str)
        with open(USERSTATES_FILE, 'w', encoding='utf-8') as states_file:
            json.dump(
                data_userstates, states_file, indent=4, ensure_ascii=False
            )

    def get_current_state(self, user_id: int):
        """Takes from base user state by self.user_id"""
        user_id = str(user_id)
        with open(USERSTATES_FILE, 'r', encoding='utf-8') as states_file:
            data_userstates = json.load(states_file)
        try:
            return data_userstates['main_users_state'][user_id]
        except KeyError:
            return False

    def is_current_state(self, user_id: int, *states):
        """Checks users's state and env check_state"""
        user_id = str(user_id)
        with open(USERSTATES_FILE, 'r', encoding='utf-8') as states_file:
            data_userstates = json.load(states_file)
        try:
            for state in states:
                if data_userstates['main_users_state'][user_id] == state:
                    return True
        except KeyError:
            return False
        return False


class UserData():
    def add_user_in_data(self, user_id: int):
        """Adds user id in data base"""
        user_id = str(user_id)
        user_data_file = get_full_data_user_path(user_id)
        with open(user_data_file, 'w+', encoding='utf-8') as ud_f:
            tmp_dict = {user_id: {}}
            json.dump(tmp_dict, ud_f, indent=4, ensure_ascii=False)

    def get_all_data_by_id(self, user_id: int):
        """Returns all data from base byt user id"""
        user_id = str(user_id)
        user_data_file = get_full_data_user_path(user_id)

        with open(user_data_file, 'r', encoding='utf-8') as ud_f:
            data_dict = json.load(ud_f)
        tmp_dict = data_dict[user_id]
        if tmp_dict:
            return tmp_dict
        return {'empty': 'empty'}

    def add_data(self, user_id: int, key, data):
        """Adds data for user_id with key"""
        user_id = str(user_id)
        user_data_file = get_full_data_user_path(user_id)

        with open(user_data_file, 'r+', encoding='utf-8') as ud_f:
            data_dict = json.load(ud_f)
            data_dict[user_id].fromkeys(key)
            data_dict[user_id][key] = data
        with open(user_data_file, 'w', encoding='utf-8') as ud_f:
            json.dump(data_dict, ud_f, indent=4, ensure_ascii=False)

    def drop_data(self, user_id: int):
        """Remove all saved user data from base"""
        user_id = str(user_id)
        user_data_file = get_full_data_user_path(user_id)

        with open(user_data_file, 'r') as ud_f:
            data_dict = json.load(ud_f)
            data_dict[user_id] = {}
        with open(user_data_file, 'w', encoding='utf-8') as ud_f:
            json.dump(data_dict, ud_f, indent=4, ensure_ascii=False)
