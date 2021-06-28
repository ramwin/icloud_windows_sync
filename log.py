import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    filename='./icloud_windows_sync/log/info.log',
    filemode='a')


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
