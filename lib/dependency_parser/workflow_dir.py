import os
from lib.dependency_parser.sql_file import SQLFile
import pdb
import json


class WorkflowDirectory:
    def __init__(self, dir):
        self.directory = dir
        self.parse_sql_files()

    def identify_sql_files(self):
        '''
            Traverses the workflow directory, looks for SQL files.
        '''
        sql_files = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                basename, extension = os.path.splitext(file)
                if extension.lower() == '.sql':
                    sql_files.append(os.path.join(root, file))

        return sql_files

    def parse_sql_files(self):
        sql_files = []
        for file in self.identify_sql_files():
            sql_files.append(SQLFile(file))

        json_data = []
        for file in sql_files:
            json_data.append(file.dict())

        with open(os.path.basename(self.directory) + '.json', 'w') as f:
            f.writelines(json.dumps(json_data, sort_keys=True, indent=4))
