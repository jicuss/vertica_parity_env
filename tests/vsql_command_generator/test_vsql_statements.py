import pdb
import unittest

import mock
from lib.vsql_command_generator.sql_statement import SQLStatement
from lib.vsql_command_generator.vertica_instance import VerticaInstance
from lib.vsql_command_generator.vsql_statement import VSQLStatement


class VSQLStatementTests(unittest.TestCase):
    def setUp(self):
        self.mock_sql_statement = mock.create_autospec(SQLStatement)
        self.mock_sql_statement.select_statement.return_value = 'SELECTSTATEMENT'
        self.mock_sql_statement.copy_statement.return_value = 'COPYSTATEMENT'
        self.mock_sql_statement.table = 'EXAMPLE_TABLE'

        self.source_vertica_instance = VerticaInstance('example_host','example_username','example_password')
        self.destination_vertica_instance = VerticaInstance('example_host2','example_username2','example_password2')

        self.vsql_command_direct = VSQLStatement(self.source_vertica_instance,self.destination_vertica_instance,self.mock_sql_statement,True)
        self.vsql_command_indirect = VSQLStatement(self.source_vertica_instance,self.destination_vertica_instance,self.mock_sql_statement)

    def tearDown(self):
        pass

    def test_direct_copy_statment(self):
        self.assertEquals(self.vsql_command_direct.copy_statement(),['vsql -U example_username -w example_password -h example_host  -d Analytics -At -F $\'\\t\' -c "SELECTSTATEMENT" | vsql -U example_username2 -w example_password2 -h example_host2 -d Analytics -c "COPYSTATEMENT"'])

    def test_indirect_copy_statment(self):
        self.assertEquals(self.vsql_command_indirect.copy_statement(),['vsql -U example_username -w example_password -h example_host  -d Analytics -At -F $\'\\t\' -c "SELECTSTATEMENT"  > EXAMPLE_TABLE.data ', 'cat EXAMPLE_TABLE.data | vsql -U example_username2 -w example_password2 -h example_host2 -d Analytics -c "COPYSTATEMENT"'])

if __name__ == '__main__':
    unittest.main()
