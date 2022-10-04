import logging
import logging.handlers
import os

class LogGen:
    @staticmethod
    def loggen():
        handler = logging.handlers.WatchedFileHandler(
            os.environ.get("LOGFILE", ".//Logs/automation.log"))
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        handler.setFormatter(formatter)
        root = logging.getLogger()
        root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        root.addHandler(handler)
        return root