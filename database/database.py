import json
from collections import OrderedDict
import os
import time
from utils.settings import Settings


class Database:
    def __init__(self):
        settings = Settings()
        self.file = settings.load_settings()['json']
        self.file_tmp = os.path.dirname(self.file) + '/.' + os.path.basename(self.file) + '.tmp'
        self.fav_file = settings.load_settings()['fav_data']

        # create data.json if doesn't exists
        if not os.path.isfile(self.file):
            data = json.dumps({}, indent=4, sort_keys=True)
            with open(self.file, 'w') as db:
                db.write(data)

    def ingest_to_json(self, dictionary, depth=None, group=None, selected_item=None):
        """
        ingest group/category
        """
        # Wait while tmp file exists
        while True:
            if not os.path.isfile(self.file_tmp):
                break
            time.sleep(3)

        # Create a tmp file to prevent render farm errors
        with open(self.file_tmp, 'w') as f:
            f.write('dictionary' + ' >> ' + dictionary)

        with open(self.file, 'r') as file:
            data = json.load(file)
        if depth == 1:
            data[group].update({dictionary:{}})
        if depth == 2:
            data[group][selected_item].update({dictionary: {}})
        if not depth:
            data.update(dictionary)

        # update item to data.json
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

        # Delete tmp file
        os.unlink(self.file_tmp)

    def read_from_json(self):
        """
        read data.json
        :return: dict
        """
        with open(self.file, 'r') as file:
            # data = json.load(file)
            data = json.load(file, object_pairs_hook=OrderedDict)
        return data

    def read_from_fav_json(self):
        """
        read fav_data.json
        :return: dict
        """
        with open(self.fav_file, 'r') as file:
            # data = json.load(file)
            data = json.load(file, object_pairs_hook=OrderedDict)
        return data

    def remove_category_from_json(self, group, depth=None, category=None, selected_sub=None):
        """
        pop group/category
        """
        # Wait while tmp file exists
        while True:
            if not os.path.isfile(self.file_tmp):
                break
            time.sleep(3)

        # Create a tmp file to prevent render farm errors
        with open(self.file_tmp, 'w') as f:
            f.write('remove_category' + ' >> ' + group)

        with open(self.file, 'r') as file:
            data = json.load(file)
        if depth is None:
            data.pop(str(group))
        if depth == 1:
            del data[str(group)][str(category)]
        if depth == 2:
            del data[str(group)][str(category)][str(selected_sub)]

        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

        # Delete tmp file
        os.unlink(self.file_tmp)

        if depth is None:
            return 'Removed %s from json' % group
        if depth == 1:
            return 'Removed %s from json' % category
        if depth == 2:
            return 'Removed %s from json' % selected_sub

    def update_category_to_json(self, updated_data, current_data, depth=None, group=None,
                                selected_sub=None):
        """
        update category
        """
        # Wait while tmp file exists
        while True:
            if not os.path.isfile(self.file_tmp):
                break
            time.sleep(3)

        # Create a tmp file to prevent render farm errors
        with open(self.file_tmp, 'w') as f:
            f.write('update_category' + ' >> ' + updated_data)

        with open(self.file, 'r') as file:
            data = json.load(file)
        if depth == 1:
            data[group][updated_data] = data[group].pop(current_data)
        if depth == 2:
            data[group][selected_sub][updated_data] = data[group][selected_sub].pop(current_data)
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

        # Delete tmp file
        os.unlink(self.file_tmp)

    def update_items_into_json(self, item, current_category, top_category, group, key, state=False):
        """
        update items to data.json
        """
        # Wait while tmp file exists
        while True:
            if not os.path.isfile(self.file_tmp):
                break
            time.sleep(3)

        # Create a tmp file to prevent render farm errors
        with open(self.file_tmp, 'w') as f:
            f.write(item + ' >> ' + key)

        # read item to data.json
        with open(self.file, 'r') as file:
            data = json.load(file)
        t = '{"%s": "%s"}' % (item, state)
        data[group][top_category][current_category][key] = json.loads(t)

        # update item to data.json
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

        # Delete tmp file
        os.unlink(self.file_tmp)

    def update_items_into_fav_json(self, item, current_category, top_category, group, key, fav=False):
        """
        update items to fav_data.json from data.json
        """
        with open(self.fav_file, 'r') as file:
            data = json.load(file)
        t = '{"%s": "%s"}' % (item, fav)
        if not group in data:
            data.update({group: {}})
        if not top_category in data[group]:
            data[group].update({top_category: {}})
        if not current_category in data[group][top_category]:
            data[group][top_category].update({current_category: {}})
        if not key in data[group][top_category][current_category]:
            data[group][top_category][current_category].update({key: {}})
        data[group][top_category][current_category][key] = json.loads(t)
        with open(self.fav_file, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def remove_item_from_json(self, current_category, top_category, group, key):
        """
        pop items from data.json
        """
        # Wait while tmp file exists
        while True:
            if not os.path.isfile(self.file_tmp):
                break
            time.sleep(3)

        # Create a tmp file to prevent render farm errors
        with open(self.file_tmp, 'w') as f:
            f.write('remove item' + ' >> ' + key)

        with open(self.file, 'r') as file:
            data = json.load(file)
        del data[group][top_category][current_category][key]
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

        # Delete tmp file
        os.unlink(self.file_tmp)

    def remove_item_from_fav_json(self, current_category, top_category, group, key):
        """
        pop items from data.json
        """
        with open(self.fav_file, 'r') as file:
            data = json.load(file)
        del data[group][top_category][current_category][key]
        with open(self.fav_file, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)