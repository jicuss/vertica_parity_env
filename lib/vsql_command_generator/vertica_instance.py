import json

import os


class VerticaInstance:
    '''
        holds username, password, host
    '''

    def __init__(self, host='', username='', password='', db='Analytics'):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.config_filepath = os.path.abspath(os.path.dirname(__file__) + '/../../config/default_credentials.json')

        ''' if the username was left blank, try and load the credentials from the config dictionary '''
        if self.host != '' and self.username == '':
            self.load_global_credential_dictionary()
            credentials = filter(lambda x: x['alias'] == self.host, self.global_credential_config)
            if len(credentials) > 0:
                self.host = credentials[0]['host']
                self.username = credentials[0]['username']
                self.password = credentials[0]['password']

    def load_global_credential_dictionary(self):
        with open(self.config_filepath, 'r') as f:
            content = f.readlines()
        self.global_credential_config = json.loads(''.join(content))

    def save_example_credential_dictionary(self):
        data = [ { "alias": "prod", "host": "pprddaavt-vip.ie.intuit.net", "password": "__PASSWORD__", "username": "jicuss" }, { "alias": "preprod", "host": "pprfdaavt-hwvip.ie.intuit.net", "password": "__PASSWORD__", "username": "jicuss" }, { "alias": "local", "host": "172.16.159.128", "password": "intuit01", "username": "dbadmin" } ]
        with open(self.config_filepath, 'w') as f:
            f.writelines(json.dumps(data, sort_keys=True, indent=4))


            VerticaInstance('prod')
            VerticaInstance('local')