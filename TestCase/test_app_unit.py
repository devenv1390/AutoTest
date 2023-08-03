__author__ = "QKY"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
import logging
import unittest

from Base.base_setting import LogsDIR, PictureDIR, ReportDIR
from Base.rewrite_funtion import only_auto_setup, only_setup_logdir


def get_parameter(log_name):
    def outer(func):
        def inner(self, *args, **kwargs):
            only_setup_logdir(LogsDIR + log_name)
            try:
                arg = func(self, *args, **kwargs)
            except Exception as e:
                print("exception: ", e)
                log(e, snapshot=True)
                raise e
            finally:
                simple_report(__file__, logpath=LogsDIR + log_name, output=ReportDIR + log_name + ".html")
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

    @get_parameter("novel")
    def test_novel(self):
        self.poco(text="健康食品知多少？").click()
        assert_exists(
            Template(PictureDIR + "tpl1690783871394.png", record_pos=(0.005, -0.939), resolution=(1080, 2340)),
            "进入动态详情页")
        keyevent("BACK")

    @get_parameter("shopping")
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
