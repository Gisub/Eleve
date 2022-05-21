import sys
import json
import os
import time
from env import *

class Convert_finished:

    def __init__(self, data):
        self.info = eval(data)
        self.data = self.info
        self.file_tmp = self.data['output'] + '.tmp'
        self.convert_finished()

    def convert_finished(self):
        if os.path.isfile(self.file_tmp):
            os.unlink(self.file_tmp)


if __name__ == "__main__":
    result = Convert_finished(sys.argv[1])
