import os
from lib.string_functions.regular_expressions import prepare_sql_statement, scan_for_froms, scan_for_inserts, \
    scan_for_joins, scan_for_updates, test_if_alias_or_table

import pdb


class SQLFile:
    def __init__(self, path):
        self.path = path
        self.file_contents = []
        self.directory = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.look_for_tables_accessed()

    def load_file(self):
        if os.path.exists(self.path):
            self.file_contents = []

            with open(self.path, 'r') as f:
                for line in f:
                    self.file_contents.append(line)

    def clean_sql(self):
        self.load_file()
        self.file_contents = map(prepare_sql_statement, self.file_contents)

    def look_for_tables_accessed(self):
        self.clean_sql()
        sql_text = ' '.join(self.file_contents)

        # remember to get rid of aliases (not real tables, just references. look for <ctg_analytics>
        inserts = filter(test_if_alias_or_table, scan_for_inserts(sql_text))
        updates = filter(test_if_alias_or_table, scan_for_updates(sql_text))
        froms = filter(test_if_alias_or_table, scan_for_froms(sql_text))
        joins = filter(test_if_alias_or_table, scan_for_joins(sql_text))

        self.accessed = []
        self.accessed.extend(froms)
        self.accessed.extend(joins)
        self.accessed = list(set(self.accessed))  # returns the unique values

        self.modified = []
        self.modified.extend(inserts)
        self.modified.extend(updates)
        self.modified = list(set(self.modified))  # returns the unique values

        for table in self.modified:
            if table in self.accessed:
                self.accessed.remove(table)

    def dict(self):
        return {
                'directory': self.directory,
                'filename': self.filename,
                'accessed': self.accessed,
                'modified': self.modified
                }
