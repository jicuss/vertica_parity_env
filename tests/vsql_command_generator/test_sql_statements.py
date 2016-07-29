import unittest

from lib.vsql_command_generator.sql_statement import SQLStatement


class SQLStatementTests(unittest.TestCase):
    def setUp(self):
        self.sql_statement = SQLStatement('example_schema.example_table', ['column1', 'column2'], ['id = 2'])
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEquals(self.sql_statement.columns, 'column1,column2')
        self.assertEquals(self.sql_statement.table, 'EXAMPLE_SCHEMA.EXAMPLE_TABLE')
        self.assertEquals(self.sql_statement.conditions, 'WHERE id = 2')
        pass

    def test_string_as_condition(self):
        # pass a string instead of array as the condition
        self.sql_statement = SQLStatement('example_schema.example_table', ['column1', 'column2'], ['id = 3'])
        self.assertEquals(self.sql_statement.conditions, 'WHERE id = 3')

    def test_pass_no_conditions_or_columns(self):
        self.sql_statement = SQLStatement('example_schema.example_table')
        self.assertEquals(self.sql_statement.columns, ' * ')
        self.assertEquals(self.sql_statement.table, 'EXAMPLE_SCHEMA.EXAMPLE_TABLE')
        self.assertEquals(self.sql_statement.conditions, '')

    def test_select_statement(self):
        self.assertEquals(self.sql_statement.select_statement(), 'SELECT column1,column2 from EXAMPLE_SCHEMA.EXAMPLE_TABLE WHERE id = 2;')

    def test_copy_statement(self):
        self.assertEquals(self.sql_statement.copy_statement(), "COPY EXAMPLE_SCHEMA.EXAMPLE_TABLE ( column1,column2 ) FROM STDIN DELIMITER E'\\011';")

if __name__ == '__main__':
    unittest.main()
