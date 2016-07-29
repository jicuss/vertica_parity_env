import unittest

from lib.vsql_command_generator.vertica_instance import VerticaInstance


class VerticaInstanceTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testVerticaConfigInstance(self):
        v = VerticaInstance('preprod')
        self.assertEquals(v.host,'pprfdaavt-hwvip.ie.intuit.net')
        v = VerticaInstance('local')
        self.assertEquals(v.host,'172.16.159.128')
        v = VerticaInstance('prod')
        self.assertEquals(v.host,'pprddaavt-vip.ie.intuit.net')



if __name__ == '__main__':
    unittest.main()
