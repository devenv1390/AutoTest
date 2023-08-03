import json
import os
import time
import sys
import platform
import base64
from functools import wraps

from BeautifulReport.BeautifulReport import ReportTestResult

HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}">
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""


class PATH:
    """ all file PATH meta """
    template_path = os.path.join(os.path.dirname(__file__), 'template')
    config_tmp_path = os.path.join(template_path, 'template.html')


class DIYMakeResultJson:
    """ make html table tags """

    def __init__(self, datas: tuple):
        """
        init self object
        :param datas: 拿到所有返回数据结构
        """
        self.datas = datas
        self.result_schema = {}

    def __setitem__(self, key, value):
        """

        :param key: self[key]
        :param value: value
        :return:
        """
        self[key] = value

    def __repr__(self) -> str:
        """
            返回对象的html结构体
        :rtype: dict
        :return: self的repr对象, 返回一个构造完成的tr表单
        """
        keys = (
            'className',
            'methodName',
            'description',
            'html_path',
            'start_time',
            'spendTime',
            'status',
            'log',
        )
        for key, data in zip(keys, self.datas):
            self.result_schema.setdefault(key, data)
        return json.dumps(self.result_schema)


class DIYReportTestResult(ReportTestResult):
    @staticmethod
    def get_testcase_property(test) -> tuple:
        """
            接受一个test, 并返回一个test的class_name, method_name, method_doc属性
        :param test:
        :return: (class_name, method_name, method_doc) -> tuple
        """
        class_name = test.__class__.__qualname__
        method_name = test.__dict__['_testMethodName']
        method_doc = test.__dict__['_testMethodDoc']
        html_path = test.__dict__['_html_path']
        start_time = test.__dict__['_start_time']
        return class_name, method_name, method_doc, html_path, start_time

    def stopTestRun(self, title=None) -> dict:
        """
            所有测试执行完成后, 执行该方法
        :param title:
        :return:
        """
        self.fields['testPass'] = self.success_counter
        for item in self.result_list:
            item = json.loads(str(DIYMakeResultJson(item)))
            self.fields.get('testResult').append(item)
        self.fields['testAll'] = len(self.result_list)
        self.fields['testName'] = title if title else self.default_report_name
        self.fields['testFail'] = self.failure_count
        self.fields['beginTime'] = self.begin_time
        end_time = int(time.time())
        start_time = int(time.mktime(time.strptime(self.begin_time, '%Y-%m-%d %H:%M:%S')))
        self.fields['totalTime'] = str(end_time - start_time) + 's'
        self.fields['testError'] = self.error_count
        self.fields['testSkip'] = self.skipped
        return self.fields


class DIYBeautifulReport(DIYReportTestResult, PATH):
    img_path = 'img/' if platform.system() != 'Windows' else 'img\\'

    def __init__(self, suites):
        super(DIYBeautifulReport, self).__init__(suites)
        self.suites = suites
        self.report_dir = None
        self.title = '自动化测试报告'
        self.filename = 'report.html'

    def report(self, description, filename: str = None, report_dir='.', log_path=None, theme='theme_default'):
        """
            生成测试报告,并放在当前运行路径下
        :param report_dir: 生成report的文件存储路径
        :param filename: 生成文件的filename
        :param description: 生成文件的注释
        :param theme: 报告主题名 theme_default theme_cyan theme_candy theme_memories
        :return:
        """
        if log_path:
            import warnings
            message = ('"log_path" is deprecated, please replace with "report_dir"\n'
                       "e.g. result.report(filename='测试报告_demo', description='测试报告', report_dir='report')")
            warnings.warn(message)

        if filename:
            self.filename = filename if filename.endswith('.html') else filename + '.html'

        if description:
            self.title = description

        self.report_dir = os.path.abspath(report_dir)
        os.makedirs(self.report_dir, exist_ok=True)
        self.suites.run(result=self)
        self.stopTestRun(self.title)
        self.output_report(theme)
        text = '\n测试已全部完成, 可打开 {} 查看报告'.format(os.path.join(self.report_dir, self.filename))
        print(text)

    def output_report(self, theme):
        """
            生成测试报告到指定路径下
        :return:
        """

        def render_template(params: dict, template: str):
            for name, value in params.items():
                name = '${' + name + '}'
                template = template.replace(name, value)
            return template

        template_path = self.config_tmp_path
        with open(os.path.join(self.template_path, theme + '.json'), 'r') as theme:
            render_params = {
                **json.load(theme),
                'resultData': json.dumps(self.fields, ensure_ascii=False, indent=4)
            }

        override_path = os.path.abspath(self.report_dir) if \
            os.path.abspath(self.report_dir).endswith('/') else \
            os.path.abspath(self.report_dir) + '/'

        with open(template_path, 'rb') as file:
            body = file.read().decode('utf-8')
        with open(override_path + self.filename, 'w', encoding='utf-8', newline='\n') as write_file:
            html = render_template(render_params, body)
            write_file.write(html)

    @staticmethod
    def img2base(img_path: str, file_name: str) -> str:
        """
            接受传递进函数的filename 并找到文件转换为base64格式
        :param img_path: 通过文件名及默认路径找到的img绝对路径
        :param file_name: 用户在装饰器中传递进来的问价匿名
        :return:
        """
        pattern = '/' if platform != 'Windows' else '\\'

        with open(img_path + pattern + file_name, 'rb') as file:
            data = file.read()
        return base64.b64encode(data).decode()

    def add_test_img(*pargs):
        """
            接受若干个图片元素, 并展示在测试报告中
        :param pargs:
        :return:
        """

        def _wrap(func):
            @wraps(func)
            def __wrap(*args, **kwargs):
                img_path = os.path.abspath('{}'.format(DIYBeautifulReport.img_path))
                os.makedirs(img_path, exist_ok=True)
                testclasstype = str(type(args[0]))
                # print(testclasstype)
                testclassnm = testclasstype[testclasstype.rindex('.') + 1:-2]
                # print(testclassnm)
                img_nm = testclassnm + '_' + func.__name__
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    if 'save_img' in dir(args[0]):
                        save_img = getattr(args[0], 'save_img')
                        save_img(os.path.join(img_path, img_nm + '.png'))
                        data = DIYBeautifulReport.img2base(img_path, img_nm + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    sys.exit(0)
                print('<br></br>')

                if len(pargs) > 1:
                    for parg in pargs:
                        print(parg + ':')
                        data = DIYBeautifulReport.img2base(img_path, parg + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    return result
                if not os.path.exists(img_path + pargs[0] + '.png'):
                    return result
                data = DIYBeautifulReport.img2base(img_path, pargs[0] + '.png')
                print(HTML_IMG_TEMPLATE.format(data, data))
                return result

            return __wrap

        return _wrap
