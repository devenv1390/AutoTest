import os

BaseDIR = os.path.dirname(os.path.dirname(__file__))
TestDataDIR = os.path.join(BaseDIR, "TestData\\")
ReportDIR = os.path.join(BaseDIR, "Report\\")
LogsDIR = os.path.join(BaseDIR, "Logs\\")
PictureDIR = os.path.join(TestDataDIR, "Picture\\")

if __name__ == '__main__':
    print(__file__)
