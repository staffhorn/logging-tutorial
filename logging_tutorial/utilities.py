# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_utilities.ipynb.

# %% auto 0
__all__ = ['SIMPLE_FORMAT', 'BETTER_FORMAT', 'SimpleFileHandler', 'SimpleScreenHandler']

# %% ../01_utilities.ipynb 5
import logging
SIMPLE_FORMAT = logging.Formatter('"%(message)s"')
BETTER_FORMAT = logging.Formatter('"%(asctime)s",%(name)s,%(funcName)s,line %(lineno)d,%(levelname)s,"%(message)s"')

class SimpleFileHandler(logging.FileHandler):
    '''
    a simple FileHandler class that uses some good defaults for the example module
    '''
    
    def __init__(self, filename='logs/example.log', **kwargs):
        # if filename is in kwargs use it, otherwise give it FILENAME
        super().__init__(filename=filename, **kwargs)
        self.setLevel(logging.INFO)
        self.setFormatter(fmt=BETTER_FORMAT)

# %% ../01_utilities.ipynb 6
class SimpleScreenHandler(logging.StreamHandler):
    import sys
    def __init__(self,stream=sys.stdout,**kwargs):
        super().__init__(stream, **kwargs)
        self.setLevel(logging.DEBUG)
        self.setFormatter(SIMPLE_FORMAT)