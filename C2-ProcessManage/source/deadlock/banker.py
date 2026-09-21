class BankerAlgorithm:    
    def __init__(self, total_resources):
        self.total = total_resources  
        self.available = total_resources.copy() 
        self.max_demand = {}
        self.allocated = {}
        self.need = {}
    
    def add_process(self, process_id, max_demand):
        self.max_demand[process_id] = max_demand
        self.allocated[process_id] = [0] * len(self.total)
        self.need[process_id] = max_demand.copy()
    
    def initial_allocation(self, process_id, allocation):
        self.allocated[process_id] = allocation
        self.available = [self.available[i] - allocation[i] for i in range(len(self.total))]
        self.need[process_id] = [self.max_demand[process_id][i] - allocation[i] for i in range(len(allocation))]
        
    def request_resources(self, process_id, request):
        print(f"Process {process_id} request: {request}")
        
        for i in range(len(request)):
            if request[i] > self.need[process_id][i]:
                print("Error: request exceeds maximum demand")
                return False
        
        for i in range(len(request)):
            if request[i] > self.available[i]:
                print("No enough resources available, request denied")
                return False
        
        old_available = self.available.copy()
        old_allocated = self.allocated[process_id].copy()
        old_need = self.need[process_id].copy()
        
        for i in range(len(request)):
            self.available[i] -= request[i]
            self.allocated[process_id][i] += request[i]
            self.need[process_id][i] -= request[i]
        
        ret, seq = self.is_safe()
        if ret:
            print("safe: request granted")
            out_seq = " -> ".join(seq)
            print(f"Safe sequence: {out_seq}")
            return True
        else:
            self.available = old_available
            self.allocated[process_id] = old_allocated
            self.need[process_id] = old_need
            print("unsafe: request denied")
            return False
    
    def is_safe(self):
        work = self.available.copy()
        finish = {pid: False for pid in self.max_demand}
        seq = []
        while True:
            found = False
            for pid in self.max_demand:
                if not finish[pid]:
                    can_allocate = True
                    for i in range(len(work)):
                        if self.need[pid][i] > work[i]:
                            can_allocate = False
                            break
                    if can_allocate:
                        for i in range(len(work)):
                            work[i] += self.allocated[pid][i]
                        finish[pid] = True
                        found = True
                        seq.append(pid)
            if not found:
                break
        
        return all(finish.values()), seq

print("\n=== Banker's Algorithm ===")
banker = BankerAlgorithm([10, 5, 7]) 

banker.add_process("P0", [7, 5, 3])
banker.initial_allocation("P0", [0, 1, 0])
banker.add_process("P1", [3, 2, 2])
banker.initial_allocation("P1", [2, 0, 0])
banker.add_process("P2", [9, 0, 2])
banker.initial_allocation("P2", [3, 0, 2])
banker.add_process("P3", [2, 2, 2])
banker.initial_allocation("P3", [2, 1, 1])
banker.add_process("P4", [4, 3, 3])
banker.initial_allocation("P4", [0, 0, 2])

print("Initial State Check:", banker.is_safe())

banker.request_resources("P1", [1, 0, 2])
banker.request_resources("P4", [3, 3, 0])
banker.request_resources("P0", [0, 1, 0])
