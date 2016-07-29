import unittest
import pdb
from lib.dependency_parser.sql_file import SQLFile

class SQLFileTests(unittest.TestCase):
    def setUp(self):
        self.sql_file = SQLFile('/Users/jicuss/Documents/TestCases/engg-etl-workflows/workflows/load_agg_customer_revenue/sql/load_agg_customer_revenue.sql')
        pass

    def tearDown(self):
        pass

    def test_look_for_tables_accessed(self):
        self.sql_file.look_for_tables_accessed()
        hash = {
            'directory': '/Users/jicuss/Documents/TestCases/engg-etl-workflows/workflows/load_agg_customer_revenue/sql',
            'accessed': ['<ctg_analytics>.fact_taxorder', '<ctg_analytics>.dim_product','<ctg_analytics>.dim_product_alias', '<ctg_analytics>.dim_bundle_rollup','<ctg_analytics>.sub_taxorder_completed_ranked'],
            'modified': ['<ctg_analytics>.agg_customer_revenue'], 'filename': 'load_agg_customer_revenue.sql'}

        for k in hash.keys():
            self.assertEquals(hash[k], self.sql_file.dict()[k])

if __name__ == '__main__':
    unittest.main()
