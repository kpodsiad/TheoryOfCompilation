from abc import ABC, abstractmethod

class ASTNode(ABC):
    def __init__(self, parent=None):
        self.value = None
        self.public_names = {}
        self.names = {}
        self.parent = parent if parent is not None else self
        if self.parent != self:
            self.public_names.update(self.parent.public_names)
            self.parent.add_child(self)
    
    @abstractmethod
    def eval(self):
        pass
    
    @abstractmethod
    def add_child(self, child):
        pass
    
    
class ASTList(ASTNode):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.children = []
        
        
    def eval(self):
        for child in self.children:
            child.eval()
            self.public_names.update(child.public_names)
            
    def add_child(self, child):
        self.children.append(child)
        

class ASTAssignment(ASTNode):
    pass


class ASTBinop(ASTNode):
    pass
        
    
class ASTFlowControl(ASTNode):
    pass
