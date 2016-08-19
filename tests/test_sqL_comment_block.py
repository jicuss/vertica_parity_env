import unittest
from lib.string_functions.sql_comments import *
import pdb

class SQLStatementExpressionTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_sql_comment_block(self):
        sql_comment_block('hello world')
        pdb.set_trace()
        pass

if __name__ == '__main__':
    unittest.main()
