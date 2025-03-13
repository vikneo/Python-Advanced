import os
import logging.config
from dict_config import dict_config

file_name = os.path.join(os.path.dirname(__file__), "logging_conf.ini")
# logging.config.fileConfig(file_name)

logging.config.dictConfig(dict_config)
app_log = logging.getLogger("appLogger")

app_log.debug("message with level DEBUG")
app_log.info("message with level INFO")
app_log.warning("message with level WARNING")
app_log.error("message with level ERROR")
app_log.critical("message with level CRITICAL")
