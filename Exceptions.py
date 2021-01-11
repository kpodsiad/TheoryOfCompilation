
class ReturnValueException(BaseException):

    def __init__(self,value):
        self.value = value
        
class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass
