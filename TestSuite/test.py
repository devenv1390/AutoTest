import unittest

from TestCase import test_app_unit

suite = unittest.TestSuite()
TestCases = unittest.TestLoader().loadTestsFromModule(test_app_unit)
suite.addTest(TestCases)
runner = unittest.TextTestRunner()
runner.run(suite)
