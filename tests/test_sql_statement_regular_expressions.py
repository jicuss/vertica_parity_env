import unittest
from lib.string_functions.sql_statement_regular_expressions import *
import pdb
import re
import pkgutil
import json


class SQLStatementExpressionTests(unittest.TestCase):
    def setUp(self):
        self.examples = json.loads(pkgutil.get_data('data','sql_regexp_examples.json'))
        pass

    def test_sql_regexp_function(self):
        m = re.findall(sql_regexp_function,self.examples['function'])
        self.assertEquals(m,[u'CTG_ANALYTICS_SRC.IS_VALID_GETDATA_EVENT'])

    def test_sql_regexp_view(self):
        m = re.findall(sql_regexp_view,self.examples['view'])
        self.assertEquals(m,[(u'CREATE  VIEW CTG_ANALYTICS_SRC.DIM_VISITOR AS\n        SELECT DIM_VISITOR.VISITOR_ID,\n        DIM_VISITOR.VISITOR_ID_SRC,\n        DIM_VISITOR.VISID_HIGH,\n        DIM_VISITOR.VISID_LOW,\n        DIM_VISITOR.VISID_HIGH_HEX,\n        DIM_VISITOR.VISID_LOW_HEX,\n        DIM_VISITOR.VISID_SOURCE_TYPE_ID,\n        DIM_VISITOR.LOAD_DATETIME\n        FROM OMT_CTG_DWH_DEV.DIM_VISITOR;', u'CTG_ANALYTICS_SRC.DIM_VISITOR'), (u'CREATE VIEW SOMETHING.JCI\n        as\n        nothign\n        ;', u'SOMETHING.JCI')])

    def test_sql_regexp_projection(self):
        m = re.findall(sql_regexp_projection,self.examples['projection'])
        self.assertEquals(m,[(u'CREATE PROJECTION CTG_ANALYTICS_SRC.DIM_TIME_BY_DAY /*+createtype(P)*/\n        (\n        DIM_TIME_BY_DAY_KEY\n        )\n        AS\n        SELECT DIM_TIME_BY_DAY.DIM_TIME_BY_DAY_KEY\n        FROM CTG_ANALYTICS_SRC.DIM_TIME_BY_DAY\n        ORDER BY DIM_TIME_BY_DAY.DIM_TIME_BY_DAY_KEY\n        UNSEGMENTED ALL NODES;', u'CTG_ANALYTICS_SRC.DIM_TIME_BY_DAY')])

    def test_sql_regexp_table(self):
        m = re.findall(sql_regexp_table,self.examples['table'])
        self.assertEquals(m,[(u'CREATE TABLE CTG_ANALYTICS.DIM_FILING_STATUS\n        (\n        FILING_STATUS_ID int NOT NULL,\n        FILING_STATUS_ABBREVIATION varchar(10) NOT NULL,\n        FILING_STATUS_DESCRIPTION varchar(255) NOT NULL,\n        BATCH_EVENT_ID int NOT NULL,\n        CREATED_TIMESTAMP timestamp NOT NULL DEFAULT statement_timestamp(),\n        UPDATED_TIMESTAMP timestamp\n        );', u'CTG_ANALYTICS.DIM_FILING_STATUS')])

        m = re.findall(sql_regexp_table,u"CREATE FLEX TABLE CTG_ANALYTICS_STG.STG_RAW_FLEX_GETDATA_UPLOAD\n(\n\n);\n")
        self.assertEquals(m,1)

    def test_sql_regexp_sequence(self):
        m = re.findall(sql_regexp_sequence,self.examples['sequence'])
        self.assertEquals(m,[(u'CREATE SEQUENCE CTG_ANALYTICS_SRC.TRN_GETDATA_FORM_FIELD_INFORMATION_SEQ ;', u'CTG_ANALYTICS_SRC.TRN_GETDATA_FORM_FIELD_INFORMATION_SEQ')])

    def test_sql_regexp_schema(self):
        m = re.findall(sql_regexp_schema,self.examples['schema'])
        self.assertEquals(m,[(u'CREATE SCHEMA CTG_ANALYTICS;', u'CTG_ANALYTICS'), (u'CREATE SCHEMA CTG_ANALYTICS_ADMIN;', u'CTG_ANALYTICS_ADMIN'), (u'CREATE SCHEMA CTG_ANALYTICS_STG;', u'CTG_ANALYTICS_STG'), (u'CREATE SCHEMA CTG_ANALYTICS_SRC;', u'CTG_ANALYTICS_SRC')])


    def test_schema_table_1(self):
        definition = 'CREATE TABLE CTG_ANALYTICS.EXAMPLE_TABLE'
        s = SchemaTable('_BASELINE','CTG_ANALYTICS.EXAMPLE_TABLE',definition)
        self.assertEquals(s.old_name,'CTG_ANALYTICS.EXAMPLE_TABLE')
        self.assertEquals(s.new_name,'CTG_ANALYTICS_BASELINE.EXAMPLE_TABLE')
        self.assertEquals(s.old_definition,'CREATE TABLE CTG_ANALYTICS.EXAMPLE_TABLE')
        self.assertEquals(s.new_definition,'CREATE TABLE CTG_ANALYTICS_BASELINE.EXAMPLE_TABLE')


        definition = 'CREATE TABLE CTG_ANALYTICS_STG.STG_TTO_ORDERS'
        s = SchemaTable('_BASELINE','CTG_ANALYTICS_STG.STG_TTO_ORDERS',definition)
        self.assertEquals(s.old_name,'CTG_ANALYTICS_STG.STG_TTO_ORDERS')
        self.assertEquals(s.new_name,'CTG_ANALYTICS_STG_BASELINE.STG_TTO_ORDERS')
        self.assertEquals(s.old_definition,'CREATE TABLE CTG_ANALYTICS_STG.STG_TTO_ORDERS')
        self.assertEquals(s.new_definition,'CREATE TABLE CTG_ANALYTICS_STG_BASELINE.STG_TTO_ORDERS')


'''
    def test_write(self):
        with open('write.json','w') as f:
            f.write(json.dumps({},sort_keys=True,indent=4, separators=(',', ': ')))
'''

if __name__ == '__main__':
    unittest.main()
