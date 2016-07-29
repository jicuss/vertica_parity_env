import unittest
from lib.string_functions.regular_expressions import *
import pdb


class RegularExpressionTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_remove_comments(self):
        string = 'select * from sometable -- this is a comment'
        self.assertEquals(remove_comments(string), 'select * from sometable ')

    def test_remove_beginning_and_trailing_spaces(self):
        string = '   select * from sometable      '
        self.assertEquals(remove_beginning_and_trailing_spaces(string), 'select * from sometable')

    def test_substitute_tab_newlines_returns(self):
        string = '\n\t\r'
        self.assertEquals(substitute_tab_newlines_returns(string), '   ')

    def test_remove_vertica_direct_comments(self):
        string = '''
                create local temporary table temp_table
                ( key )
                on commit preserve rows as
                /*+ direct */ select * from some_other_table
        '''
        self.assertEquals(remove_vertica_direct_comments(string),'\n                create local temporary table temp_table\n                ( key )\n                on commit preserve rows as\n                  select * from some_other_table\n        ')

    def test_remove_brackets_before_table(self):
        '''
            some views have brackets before the table name. remove those
            example: FROM ((CTG_ANALYTICS.SUB_CUSTOMER_SEGMENT a
        '''
        string = '''
                CREATE  VIEW CTG_ANALYTICS_WS.rj_sub_customer_segment AS
         SELECT a.CUSTOMER_KEY,
                a.TAX_YEAR,
                a.CUSTOMER_TYPE_ID,
                a.CUSTOMER_DEFINITION_ID,
                c.CUSTOMER_TYPE_ROLLUP,
                c.CUSTOMER_TYPE,
                b.CUSTOMER_DEFINITION
         FROM ((CTG_ANALYTICS.SUB_CUSTOMER_SEGMENT a LEFT JOIN CTG_ANALYTICS.DIM_CUSTOMER_DEFINITION b ON ((a.CUSTOMER_DEFINITION_ID = b.CUSTOMER_DEFINITION_ID))) LEFT JOIN CTG_ANALYTICS.DIM_CUSTOMER_TYPE c ON ((a.CUSTOMER_TYPE_ID = c.CUSTOMER_TYPE_ID)));
        '''
        self.assertEquals(scan_for_froms(string), ['ctg_analytics.sub_customer_segment'])

    def test_add_space_after_string(self):
        string = 'something)'
        self.assertEquals(add_space_after_string(string), 'something )')
        string = 'something('
        self.assertEquals(add_space_after_string(string), 'something (')

    def test_add_space_before_string(self):
        string = '(something'
        self.assertEquals(add_space_before_string(string), '( something')
        string = ')something'
        self.assertEquals(add_space_before_string(string), ') something')

    def test_prepare_sql_statement(self):
        string = '''
                create local temporary table temp_table
                ( key )
                on commit preserve rows as
                /*+ direct */ select * from some_other_table
        '''
        self.assertEquals(prepare_sql_statement(string),'create local temporary table temp_table ( key ) on commit preserve rows as select * from some_other_table')

    def test_scan_for_inserts(self):
        string = '''
            insert into example_table(key1)
            select * from something_else;
            insert into a_second_example_table(key1)
            select * from something_else;
        '''

        self.assertEquals(scan_for_inserts(string), ['example_table', 'a_second_example_table'])

    def test_scan_for_updates(self):
        string = '''
            update example_table(key1)
            select * from something_else;
            update  a_second_example_table(key1)
            select * from something_else;
        '''

        self.assertEquals(scan_for_updates(string), ['example_table', 'a_second_example_table'])

    def test_scan_for_froms(self):
        string = '''
            select * from sometable
            inner join another_table
            left join a_third_table
        '''

        self.assertEquals(scan_for_froms(string), ['sometable'])

    def test_scan_for_joins(self):
        string = '''
            select * from sometable
            inner join another_table
            left join a_third_table
        '''
        results = scan_for_joins(string)
        for table in ['another_table', 'a_third_table']:
            self.assertIn(table, results)

    def test_test_if_alias_or_table(self):
        self.assertFalse(test_if_alias_or_table('something'))
        self.assertTrue(test_if_alias_or_table('something.something'))
        self.assertTrue(test_if_alias_or_table('<something>.something'))

if __name__ == '__main__':
    unittest.main()
