# used to find SQL statements that match a pattern
import re
import pdb

class SchemaTable:
    def __init__(self,suffix,name,definition = None):
        self.suffix = suffix.upper()
        self.old_name = name
        self.old_definition = definition
        self.new_name = str(self.old_name).upper()
        self.new_definition = str(self.old_definition)
        self.new_schema_list = []
        self.replace_schema()

    def replace_schema(self):
        schemas = ["CTG_ANALYTICS_STG", "CTG_ANALYTICS_SRC", "CTG_ANALYTICS", "CTG_ANALYTICS_ADMIN",'OMT_CTG_DWH']
        for schema in schemas:
            new_schema = schema + self.suffix
            if new_schema not in self.new_schema_list:
                self.new_schema_list.append(new_schema)

            self.new_name = re.sub(schema + r'\.',new_schema + '.',self.new_name)
            self.new_definition = re.sub(schema + r'\.',new_schema + '.',self.new_definition)

sql_regexp_schema = r'(CREATE\s+SCHEMA\s+(\S+)\;)'
sql_regexp_sequence = r'(CREATE\s+SEQUENCE\s+(\S+)[\s|\S]+?\;)'
sql_regexp_sequence_ref = 'nextval\(\'(\S+)?\'\)'
sql_regexp_table = r'(CREATE\s+[FLEX\s+]*TABLE\s+(\S+)[\s|\S]+?\;)'
sql_regexp_projection = r'(CREATE\s+PROJECTION\s+(\S+)[\s|\S]+?\;)'
sql_regexp_view = r'(CREATE\s+VIEW\s+(\S+)[\s|\S]+?\;)'
sql_regexp_function = r'CREATE\s+FUNCTION\s+(\S+)\('
