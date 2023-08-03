import os
import shutil

from airtest.core.api import connect_device
from airtest.core.helper import G
from airtest.core.settings import Settings as ST


def only_auto_setup(basedir=None, devices=None, project_root=None, compress=None):
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
    if project_root:
        ST.PROJECT_ROOT = project_root
    if compress:
        ST.SNAPSHOT_QUALITY = compress


def only_setup_logdir(logdir):
    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.mkdir(logdir)
    ST.LOG_DIR = logdir
    G.LOGGER.set_logfile(os.path.join(ST.LOG_DIR, ST.LOG_FILE))
