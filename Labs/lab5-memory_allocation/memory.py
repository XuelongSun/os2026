class MemoryBlock:
    def __init__(self, start, length):
        self.name = None
        self.start = start
        self.length = length
        self.free = True
    
    def mark_allocated(self, name):
        self.name = name
        self.free = False


class Memory:
    def __init__(self, size=100):
        self.size = size #KB
        self.blocks: list[MemoryBlock] = []
        
    def allocate(self, start, length):
        raise NotImplementedError("Allocate method not implemented")
    
    def deallocate(self, start, length):
        raise NotImplementedError("Deallocate method not implemented")

    def reset(self):
        raise NotImplementedError("Reset method not implemented")


class FixedMemory(Memory):
    def __init__(self, size, block_size):
        """block_size: if it is a number, it means fixed partition size;
        if it is a list, it means variable partition sizes.
        """
        super().__init__(size)
        self.block_size = block_size
    
    def allocate(self, name, size):
        pass
    
    def deallocate(self, start):
        pass
    
    def reset(self):
        pass


class DynamicMemory(Memory):
    def __init__(self, size, policy="first-fit"):
        super().__init__(size)
        self.blocks.append(MemoryBlock(0, size))
        self.policy = policy
    
    def allocate(self, name, size):
        pass
    
    def deallocate(self, start):
        pass
    
    def reset(self):
        pass
    
    