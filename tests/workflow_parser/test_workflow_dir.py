import unittest
from lib.dependency_parser.workflow_dir import WorkflowDirectory

class WorkflowDirectoryTests(unittest.TestCase):
    def setUp(self):
        #self.wd = WorkflowDirectory('/Users/jicuss/Documents/TestCases/engg-etl-workflows/load_agg_customer_revenue')
        self.wd = WorkflowDirectory('/Users/jicuss/Documents/TestCases/engg-etl-workflows/load_fact_accepted_return')

    def tearDown(self):
        pass

    def test_identify_sql_files(self):
        self.assertEquals(self.wd.identify_sql_files(),['/Users/jicuss/Documents/TestCases/engg-etl-workflows/load_agg_customer_revenue/sql/load_agg_customer_revenue.sql'])

if __name__ == '__main__':
    unittest.main()
