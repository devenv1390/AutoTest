__author__ = "QKY"

import time

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
import logging
import unittest

from Base.base_setting import LogsDIR, PictureDIR, ReportDIR
from Base.airtest_rewrite import only_auto_setup, only_setup_logdir


def get_parameter(*_args, **_kwargs):
    def outer(func):
        def inner(self, *args, **kwargs):
            only_setup_logdir(LogsDIR + _kwargs['log_name'])
            self.__dict__['_start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            try:
                arg = func(self, *args, **kwargs)
            except Exception as e:
                print("exception: ", e)
                log(e, snapshot=True)
                raise e
            finally:
                simple_report(__file__, logpath=LogsDIR + _kwargs['log_name'],
                              output=ReportDIR + _kwargs['log_name'] + ".html")
                self.__dict__['_html_path'] = ReportDIR + _kwargs['log_name'] + ".html"
                self.__dict__['_testMethodDoc'] = _kwargs['case_desc']
                while not self.poco(text="康康Need").exists():
                    keyevent("BACK")
            return arg

        return inner

    return outer


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        logger = logging.getLogger("airtest")
        logger.setLevel(logging.ERROR)
        if not cli_setup():
            only_auto_setup(__file__, devices=[
                "Android:///"
            ])
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

        print("start app...")
        start_app("com.example.kkneed")
        sleep(1)

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        stop_app("com.example.kkneed")

    @get_parameter(log_name="novel", case_desc="测试文章详情页")
    def test_novel(self):
        self.poco(text="健康食品知多少？").click()
        assert_exists(
            Template(PictureDIR + "tpl1690783871394.png", record_pos=(0.005, -0.939), resolution=(1080, 2340)),
            "进入动态详情页")
        keyevent("BACK")

    @get_parameter(log_name="shopping", case_desc="测试商城页")
    def test_shopping(self):
        self.poco("androidx.compose.ui.platform.ComposeView").child("android.view.View").child(
            "android.view.View").child(
            "android.view.View").child("android.view.View").child("android.view.View")[1].child(
            "android.view.View").click()
        assert_exists(
            Template(PictureDIR + "tpl1690784399694.png", record_pos=(-0.01, -0.141), resolution=(1080, 2340)),
            "进入商城")
        keyevent("BACK")


if __name__ == '__main__':
    unittest.main()
