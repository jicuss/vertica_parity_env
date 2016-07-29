from lib.vsql_command_generator.sql_statement import SQLStatement
from lib.vsql_command_generator.vertica_instance import VerticaInstance


class VSQLStatement:
    def __init__(self, source_vertica_instance, destination_vertica_instance, sql_statement, direct_copy=False):

        # review this approach
        correct_input_types = True
        if not isinstance(source_vertica_instance, VerticaInstance):
            correct_input_types = False
        if not isinstance(destination_vertica_instance, VerticaInstance):
            correct_input_types = False
        if not isinstance(sql_statement, SQLStatement):
            correct_input_types = False
        if not correct_input_types:
            raise TypeError, 'Incorrect Input Datatypes'

        self.source_vertica_instance = source_vertica_instance
        self.destination_vertica_instance = destination_vertica_instance
        self.sql_statement = sql_statement
        self.direct_copy = direct_copy

    def copy_statement(self):
        destination = self.sql_statement.table
        cmd_download = "vsql -U {} -w {} -h {}  -d {} -At -F $'\\t' -c \"{}\"".format(
                self.source_vertica_instance.username,
                self.source_vertica_instance.password,
                self.source_vertica_instance.host,
                self.source_vertica_instance.db,
                self.sql_statement.select_statement()
        )

        cmd_upload = "vsql -U {} -w {} -h {} -d {} -c \"{}\"".format(
                self.destination_vertica_instance.username,
                self.destination_vertica_instance.password,
                self.destination_vertica_instance.host,
                self.destination_vertica_instance.db,
                self.sql_statement.copy_statement()
        )

        output = []
        if self.direct_copy:
            output.append('{} | {}'.format(cmd_download, cmd_upload))
        else:
            output.append("{}  > {}.data ".format(cmd_download, destination))
            output.append('cat {}.data | {}'.format(destination, cmd_upload))
        return output