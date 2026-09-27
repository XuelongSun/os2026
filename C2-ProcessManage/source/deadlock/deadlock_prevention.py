import threading
import time

class Resource:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.owner = None
        
    def acquire(self, owner):
        print(f"{owner} ==> {self.name}")
        self.lock.acquire()
        self.owner = owner
        print(f"{owner} 🔒 {self.name}")
        return True
    
    def acquire_with_timeout(self, owner, timeout=2):
        print(f"{owner} ==> {self.name} ({timeout}s)")
        acquired = self.lock.acquire(timeout=timeout)
        if acquired:
            self.owner = owner
            print(f"{owner} 🔒 {self.name}")
        else:
            print(f"{owner} ❌ {self.name} (timeout)")
        return acquired
    
    def release(self):
        if self.lock.locked():
            print(f"{self.owner} 🔓 {self.name}")
            self.owner = None
            self.lock.release()

resources = {
    "printer": Resource("🖨️"),
    "disk": Resource("💾"),
}

class NumberResource(Resource):
    def __init__(self, name, num):
        super().__init__(name)
        self.N = num

num_resources = {
    "printer": NumberResource("🖨️", 2),
    "disk": NumberResource("💾", 1),
}

def worker(name, needed_resources):
    for res in needed_resources:
        resources[res].acquire(name)
        time.sleep(1)
    print(f"{name}: ✅")
    for res in needed_resources:
        resources[res].release()

def safe_worker_bhw(name, needed_resources):
    for res in needed_resources:
        resources[res].acquire(name)
    time.sleep(1)
    print(f"{name}: ✅")

    for res in needed_resources:
        resources[res].release()

def safe_worker_bp(name, needed_resources):
    while(1):
        acquired = []
        for res in needed_resources:
            if resources[res].acquire_with_timeout(name):
                acquired.append(res)
                time.sleep(1)
            else:
                for res in needed_resources:
                    resources[res].release()
                acquired = []
        if len(acquired) == len(needed_resources):
            time.sleep(1)
            print(f"{name}: ✅")
            for res in needed_resources:
                resources[res].release()
            break

def safe_worker_bcw(name, needed_resources):
    # Enforce a global order: printer < disk
    sorted_resources = sorted(needed_resources,
                              key=lambda r: num_resources[r].N)
    for res in sorted_resources:
        resources[res].acquire(name)
        time.sleep(1)
    time.sleep(1)
    print(f"{name}: ✅")
    for res in needed_resources:
        resources[res].release()
            
if __name__ == "__main__":
    thread1 = threading.Thread(target=safe_worker_bhw, args=("A", ["printer", "disk"]))
    thread2 = threading.Thread(target=safe_worker_bhw, args=("B", ["disk", "printer"]))
    thread1.start()
    thread2.start()
    thread1.join() 
    thread2.join()
