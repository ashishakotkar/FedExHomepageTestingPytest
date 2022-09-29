import logging

class LogGen:
    @staticmethod
    def loggen():
        logFileFormatter = logging.Formatter(
            fmt=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger=logging.getLogger()
        logger.setLevel(logging.INFO)
        fileHandler = logging.FileHandler(filename='.\\Logs\\automation.log')
        fileHandler.setLevel(level=logging.INFO)
        logger.addHandler(fileHandler)

        return logger