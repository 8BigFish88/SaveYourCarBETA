import logging, coloredlogs
from app.settings.loggings.messages import Log

coloredlogs.install()
log = Log()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh = logging.FileHandler(log.filename, mode=log.mode)
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt=log.level, datefmt=log.dateFmt)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)