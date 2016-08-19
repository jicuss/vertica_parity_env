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

        total = []
        total_h = {
                'directory': 'all',
                'filename': 'all',
                'accessed': [],
                'modified': []
                }

        for file in sql_files:
            for k in ['accessed','modified']:
                total_h[k] += file.dict()[k]
                total_h[k] = list(set(total_h[k]))
                total_h[k].sort()

        total_h['accessed'] = filter(lambda x: x not in total_h['modified'],total_h['accessed'])

        json_data.append(total_h)

        with open(os.path.basename(self.directory) + '.json', 'w') as f:
            f.writelines(json.dumps(json_data, sort_keys=True, indent=4))
