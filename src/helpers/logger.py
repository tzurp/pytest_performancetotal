import logging

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("performancetotal")

    def debug(self, message: object):
        self.logger.debug(message)
    
    def info(self, message: object):
        self.logger.info(message)
    
    def error(self, message: object):
        self.logger.error(message)