import unittest

from BeautifulReport import BeautifulReport

from TestCase import test_app_unit

suite = unittest.TestSuite()
TestCases = unittest.TestLoader().loadTestsFromModule(test_app_unit)
suite.addTest(TestCases)
# runner = unittest.TextTestRunner()
# runner.run(suite)
runner = BeautifulReport(suite)
runner.report("测试报告", "report.html")
