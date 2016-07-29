import pdb

class SQLStatement:
    '''
        holds a list of desired columns and a destination table
        Methods:
                select statement
                copy statement

    '''
    def __init__(self, table='', columns=[], conditions=[]):

        if len(columns) > 0:
            self.columns = (',').join(columns)
        else:
            self.columns = ' * '

        self.table = table.upper()

        if len(conditions) > 0:
            if type(conditions) in (unicode, str):
                self.conditions = "WHERE {}".format(conditions)
            if type(conditions) is list:
                self.conditions = "WHERE {}".format((' AND ').join(conditions))
        else:
            self.conditions = ''

    def select_statement(self):
        return "SELECT {} from {} {};".format(self.columns, self.table, self.conditions)

    def copy_statement(self):
        if self.columns != ' * ':
            columns = '( {} )'.format(self.columns)
        else:
            columns = ''

        return "COPY {} {} FROM STDIN DELIMITER E'\\011';".format(self.table, columns)
