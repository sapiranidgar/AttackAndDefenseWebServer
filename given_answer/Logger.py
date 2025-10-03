import logging
import logging.config
from enum import Enum

class LogType(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

'''
Logger class, handles adding lines to the debug
'''
class Logger:
    
    def __init__(self):   
        logging.config.fileConfig('loggingConfig.conf')
        self.logger = logging.getLogger('Logger')

    def add_log(self, line : str, code: str)->None:
        '''
        Function that gets a line and a log code and add the line to the debug with the correct code (INFO, DEBUG etc .. )
        '''

        if not isinstance(code, LogType):
            self.logger.error(f"Invalid log type: {code}. Must be an instance of LogType.")
            raise ValueError(f"Invalid log type: {code}. Must be an instance of LogType.")
        
        self.logger.log(code.value, line)