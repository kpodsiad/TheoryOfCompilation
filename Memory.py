class Memory:
    def __init__(self, name): # memory name
        self.bindings = {}
        self.name = name
   
    def has_key(self, name):  # variable name
        return name in self.bindings
   
    def get(self, name):         # gets from memory current value of variable <name>
        return self.bindings[name]
   
    def put(self, name, value):  # puts into memory current value of variable <name>
        self.bindings[name] = value
   

class MemoryStack:                                          
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        if memory is None:
            self.frames = [Memory('globals')]
        else:
            self.frames = [memory]
    
    def get(self, name):             # gets from memory stack current value of variable <name>
        for frame in self.frames[::-1]:
            if frame.has_key(name):
                return frame.get(name)
        raise NameError(f'Name {name} is not defined')
    
    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.frames[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>. If variable <name> doesn't exist insert to current stack
        for frame in self.frames[::-1]:
            if frame.has_key(name):
                return frame.put(name, value)
        self.insert(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.frames.append(memory)
    
    def pop(self):          # pops the top memory from the stack
        self.frames.pop(-1)

