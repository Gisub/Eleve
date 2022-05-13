
from database.env import *
import os
import json


class Settings:

    def __init__(self):

        self.pref = config['PATH_PERSONAL_CONFIG']
        self.fav_data = config['fav_data']

        # create root directory
        if not os.path.isdir(os.path.dirname(self.pref)):
            os.makedirs(os.path.dirname(self.pref))

        # create settings.json with default values
        if not os.path.isfile(self.pref):
            self.write_default_settings()

        # create fav_data.json with default values
        if not os.path.isfile(self.fav_data):
            self.write_fav_data()

    def write_settings(self, category, stay_top):
        """
        write default / user settings into settings.json
        """
        with open(self.pref, 'w') as file:
            dict_str = json.dumps({
                        "category": "{}".format(category),
                        "stay_top": "{}".format(stay_top)
                    }
            )
            file.write(dict_str)

    def load_settings(self):
        """
        open and return settings.json
        """
        with open(self.pref, 'r') as s:
            personal_file = json.load(s)

        for k in personal_file.keys():
            config[k] = personal_file[k]

        return config

    def write_default_settings(self):
        """
        default settings.
        """
        self.write_settings(
            'Comp_Source',
            True
        )

    def write_fav_data(self):
        """
        default fav_data.
        """
        data = json.dumps({}, indent=4)
        with open(self.fav_data, 'w') as db:
            db.write(data)
