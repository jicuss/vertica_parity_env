'''
    The aim here is to generate a set of VSQL commands that will export data form vertica and import into a local vertica instance
    options
    - store the data in a local file or pipe the data directly into the local vertica instance
    - username and password credentials
'''
import datetime
import logging
import os
import json
from lib.vsql_command_generator.sql_statement import SQLStatement
from lib.vsql_command_generator.vertica_instance import VerticaInstance
from lib.vsql_command_generator.vsql_statement import VSQLStatement

logger = logging.getLogger('')

def generateExampleCopyJSON():
    output = {'tables': []}

    for table in ["ctg_analytics.dim_upsell_information", "ctg_analytics.dim_sku_rollup", "ctg_analytics.dim_upsell_offer", "ctg_analytics.dim_tax_date"]:
        output['tables'].append({'name': table})

    for table in ["ctg_analytics.fact_clickstream_upsell", "ctg_analytics.sub_clickstream_tt_start_first", "ctg_analytics.fact_auth_id_start_sku", "ctg_analytics.fact_sku_selection", "ctg_analyst_layer.auth_analytics_base", "ctg_analytics.fact_auth_id_completed_sku"]:
        output['tables'].append({'name': table,'conditions':['auth_id in (select auth_id from CTG_ANALYTICS_WS.AGG_CUSTOMER_REVENUE_JICUSS_SELECTIONS)','auth_id = 5']})

    with open('output.json','w') as f:
        f.write(json.dumps(output, sort_keys=True, indent=4))


def main(jsonPath, logLevel, logFile):
    logFormat = '%(asctime)s : filename=%(filename)s : threadname=%(threadName)s : linenumber=%(lineno)d : messageType=%(levelname)s : %(message)s'

    logging.basicConfig(filename=logFile, filemode='a+', level=logLevel, format=logFormat)

    '''
    Forces logging to the console so user can track progress
    '''
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logging.info('Attempting to Generate VSQL Copy Commands')

    with open(jsonPath, 'r') as f:
        content = f.readlines()
    copy_config = json.loads(''.join(content))

    output = []
    source = VerticaInstance('prod')
    dest = VerticaInstance('local')

    for table in copy_config['tables']:
        if 'conditions' in table:
            sql = SQLStatement(table['name'], [], table['conditions'])
        else:
            sql = SQLStatement(table['name'])

        for line in VSQLStatement(source, dest, sql).copy_statement():
            output.append(line)

    output.sort()
    with open(jsonPath + '_copy_commands.txt', 'w') as f:
        for line in output:
            f.write(line + '\n')


if __name__ == "__main__":
    log_path = os.path.abspath(os.path.join(__file__, '..', 'logs/'))
    main(logging.DEBUG, log_path + '/' + str(datetime.datetime.now().isoformat()) + "-workflow_parser.log")
