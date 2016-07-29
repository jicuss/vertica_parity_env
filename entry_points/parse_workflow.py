import datetime
import logging
import os
from lib.dependency_parser.workflow_dir import WorkflowDirectory


logger = logging.getLogger('')


def main(workflowDir,logLevel, logFile):
    logFormat = '%(asctime)s : filename=%(filename)s : threadname=%(threadName)s : linenumber=%(lineno)d : messageType=%(levelname)s : %(message)s'

    logging.basicConfig(filename=logFile, filemode='a+', level=logLevel, format=logFormat)

    '''
    Forces logging to the console so user can track progress
    '''
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logging.info('Parsing Workflow')
    WorkflowDirectory(workflowDir)


if __name__ == "__main__":
    log_path = os.path.abspath(os.path.join(__file__, '..', 'logs/'))
    main(logging.DEBUG, log_path + '/' + str(datetime.datetime.now().isoformat()) + "-workflow_parser.log")
