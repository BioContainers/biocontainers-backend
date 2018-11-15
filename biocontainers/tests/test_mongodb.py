import unittest

from pymodm.connection import _get_db
from pymodm import connect

from biocontainers.common.models import MongoTool, MongoToolVersion


class TestAll(unittest.TestCase):

    def setUp(self):
        connect("mongodb://localhost:27017/unittest")
        self.tool1 = MongoTool()
        self.tool1.id = "tool-1"
        self.tool1.name = "tool-1"
        self.tool1.description = "PeptideShaker is a search engine independent platform for interpretation of proteomics identification results from multiple search engines," \
                                 "currently supporting X!Tandem, MS-GF+, MS Amanda, OMSSA, MyriMatch, Comet, Tide, Mascot, Andromeda and mzIdentML. " \
                                 "By combining the results from multiple search engines, while re-calculating PTM localization scores and redoing the protein inference," \
                                 "PeptideShaker attempts to give you the best possible understanding of your proteomics data"
        self.tool1.save()
        self.tool2 = MongoTool()
        self.tool2.id = "tool-2"
        self.tool2.name = "tool-2"
        self.tool2.tool_classes = ['TOOL']
        self.tool2.save()
        self.assertTrue(len(self.tool2.tool_classes) == 1)


    def test_01_func(self):
        self.tool_version = MongoToolVersion()
        self.tool_version.id = "version-1"
        self.tool_version.name = "tool-1"
        self.tool_version.ref_tool = self.tool1
        self.tool_version.save()
        self.assertEqual(self.tool1.id, "tool-1")
        self.assertTrue(len(self.tool1.get_tool_versions()) == 1)


    def tearDown(self):
        _get_db().client.drop_database('unittest')

if __name__ == '__main__':
    unittest.main()
