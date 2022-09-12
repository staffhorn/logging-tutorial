# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_examples.ipynb.

# %% auto 0
__all__ = ['SIMPLE_FORMAT', 'BETTER_FORMAT', 'SUBJECT', 'example_01', 'example_02', 'example_03', 'example_04', 'example_05',
           'example_06_get_logger', 'example_06_configure_handler', 'example_06', 'example_07_get_logger', 'example_07',
           'SimpleFileHandler', 'SimpleScreenHandler', 'example_08', 'SimpleGMailHandler', 'example_09', 'logger_timer',
           'example_10']

# %% ../00_examples.ipynb 3
import logging
from logging.handlers import SMTPHandler
import os
import sys

'''
Some module level setup
'''

SIMPLE_FORMAT = logging.Formatter('"%(message)s"')
BETTER_FORMAT = logging.Formatter('"%(asctime)s",%(name)s,%(funcName)s,line %(lineno)d,%(levelname)s,"%(message)s"')

# %% ../00_examples.ipynb 4
def example_01() -> None:
    '''
    Example 01
    Print debugging to the screen using print()
    '''
    print('This debug message uses print.')

# %% ../00_examples.ipynb 7
def example_02() -> None:
    '''
    Example 02
    Log to the screen instead of print.

    '''
    logging.basicConfig(level="DEBUG")
    logging.debug('This message uses the root logger.')

# %% ../00_examples.ipynb 10
def example_03() -> None:
    '''
    Example 03
    Find the root logger, change its level to INFO, and add better formatting.
    '''
    root_logger = logging.getLogger()
    root_logger.setLevel("INFO")
    root_logger.handlers[0].setFormatter(BETTER_FORMAT)
    logging.info('This better format adds context information to each message.')

# %% ../00_examples.ipynb 13
def example_04() -> None:
    '''
    Example 04
    Use a named logger with customized properties.
    '''

    # Let's create a custom logger, my_logger.
    my_logger = logging.getLogger(__name__)
    my_logger.setLevel(logging.DEBUG)
    logging.info('This INFO message will display.')
    logging.debug('We will not see this because DEBUG is lower than the root level INFO.')

    my_logger = logging.getLogger(__name__)
    my_logger.debug('The __main__ logger is set to a level of DEBUG, so this message displays.')
    my_logger.info('Note the __main__ logger uses the format from root.')
    my_logger.handlers = []



# %% ../00_examples.ipynb 15
def example_05() -> None:
    '''
    Example 05
    Log to a file with print()
    '''


    with open(file='example_print.log', mode='a') as file:
        print('This is an example of writing to a logfile with print.', file=file)

# %% ../00_examples.ipynb 17
def example_06_get_logger(level:int=logging.INFO) -> None:
    '''
    Example 06
    Customize our logger with a file handler and a formatter.
    '''
    logger =  logging.getLogger(__name__)
    logger.handlers.clear()
    logger.propagate = False
    return logger
    
def example_06_configure_handler(
    filename:str=None, 
    format:logging.Formatter=SIMPLE_FORMAT, 
    level:int=logging.INFO) -> logging.Handler:
    
    if filename is not None:
        handler = logging.FileHandler(filename=filename, mode='a')
        handler.setFormatter(fmt=BETTER_FORMAT)
        handler.setLevel(level)
    else:
        handler = None
    return handler

def example_06():
    '''
    Example 06
    Create and customize a file logger with a logging.Handler that
    sends log messages to a file and add a custom formatter
    '''
    FILENAME='logs/example_06.log'

    logger = example_06_get_logger(level=logging.INFO) # the screen handler won't show debug messages

    logger.addHandler(
        example_06_configure_handler(format=BETTER_FORMAT, 
                                     filename=FILENAME, 
                                     level=logging.DEBUG)) # the file handler WILL show debug messages.

    logger.debug(f"Debug messages go to the file {FILENAME}")


# %% ../00_examples.ipynb 19
'''
Example 07
A logger that sends debug messages to the screen and info messages to a file
'''

def example_07_get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger

def example_07():
    FILENAME='logs/example_07.log'
    logger = example_07_get_logger()
    logger.handlers.clear()
    logger.addHandler(SimpleScreenHandler())
    logger.addHandler(SimpleFileHandler(filename='logs/example_07.log'))

    logger.debug('debug messages just go to the screen.  The screen format is simply the message.')
    logger.info("Info messages go to screen and file. The file format has more information.")



# %% ../00_examples.ipynb 20
class SimpleFileHandler(logging.FileHandler):
    '''
    a simple FileHandler class that uses some good defaults for the example module
    '''
    
    def __init__(self, filename='logs/example.log', **kwargs):
        # if filename is in kwargs use it, otherwise give it FILENAME
        super().__init__(filename=filename, **kwargs)
        self.setLevel(logging.INFO)
        self.setFormatter(fmt=BETTER_FORMAT)
        
class SimpleScreenHandler(logging.StreamHandler):
    '''
    a simple StreamHandler class with good defaults that sends text to stdout
    '''
    import sys
    def __init__(self,stream=sys.stdout,**kwargs):
        super().__init__(stream, **kwargs)
        self.setLevel(logging.DEBUG)
        self.setFormatter(fmt=SIMPLE_FORMAT)

# %% ../00_examples.ipynb 23
def example_08() -> None:
    '''
    Example 08
    Create a tree view of the logger data structure using the python logging_tree module.
    '''
    import logging_tree

    logger = example_07_get_logger()
    logger.handlers.clear()
    logger.addHandler(SimpleScreenHandler())
    logger.addHandler(SimpleFileHandler('logs/example_08.log'))
    logging_tree.printout()


# %% ../00_examples.ipynb 25
'''
Example 09
Configure logging to send email via a gmail account.
'''

SUBJECT='Alert'

class SimpleGMailHandler(SMTPHandler):

    def __init__(self, **kwargs):
        
        import os
        kwargs.setdefault('mailhost', ('smtp.gmail.com',587))
        try: 
            fromaddr = kwargs.setdefault('fromaddr', os.environ['gmail_app_sender'])
            kwargs.setdefault('credentials', (fromaddr, os.environ['gmail_app_pass']))
        except Exception as e:
            logging.ERROR("You haven't set the gmail credentials.")
            raise e
        kwargs.setdefault('toaddrs', [fromaddr])
        kwargs.setdefault('subject',f'ALERT from {__name__}')
        kwargs.setdefault('secure',())

        super().__init__(**kwargs)

        self.setFormatter(fmt=BETTER_FORMAT)
        self.setLevel(logging.ERROR)

def example_09():
    '''
    Test a logger with a simple SMTP handler.
    '''
    logger = logging.getLogger(__name__)
    logger.handlers = []
    logger.addHandler(SimpleGMailHandler())
    logger.error('''Simulated alert. There is no emergency.''')

# %% ../00_examples.ipynb 27
'''
Example 10
Using time module to see which logging handlers take a long time.
'''

import logging
from time import perf_counter
import sys


def logger_timer(logger: logging.Logger, level:int, message:str) -> float:
    '''
    logger_timer()
    measures the time taken to log a message using perf_counter
    '''
    tic = perf_counter()
    logger.log(level, message)
    toc = perf_counter()
    return toc-tic

def example_10():
    '''
    Example 10
    Test the time required to log to STDOUT, a file, and email.
    '''
    
    file_logger = logging.getLogger('File')
    file_logger.setLevel(logging.INFO)
    file_logger.addHandler(SimpleFileHandler())
    smtp_logger = logging.getLogger('SMTP')
    smtp_logger.setLevel(logging.ERROR)
    smtp_logger.addHandler(SimpleGMailHandler())

    # Get time for each type of logging handler

    stream_time = logger_timer(logging.root, logging.DEBUG, 'Stream to stdout')
    file_time = logger_timer(file_logger, logging.INFO, 'File logger.')
    smtp_time = logger_timer(smtp_logger, logging.ERROR, 'SMTP logger.')

    # print times

    logging.info(f"Stream logger_timer {stream_time:0.4f} seconds.")
    logging.info(f"File logger_timer   {file_time:0.4f} seconds.")
    logging.info(f"SMTP logger_timeer   {smtp_time:0.4f} seconds.")

