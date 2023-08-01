import os

from airtest.core.api import connect_device
from airtest.core.helper import G, set_logdir
from airtest.utils.compat import script_log_dir


def only_auto_setup(basedir=None, devices=None):
    """
    只对设备进行初始化连接
    """
    if basedir:
        if os.path.isfile(basedir):
            basedir = os.path.dirname(basedir)
        if basedir not in G.BASEDIR:
            G.BASEDIR.append(basedir)
    if devices:
        for dev in devices:
            connect_device(dev)


def only_setup_logdir(basedir=None, logdir=None):
    """
    只对logdir进行设置
    """
    if logdir:
        logdir = script_log_dir(basedir, logdir)
        set_logdir(logdir)
