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

    def release(self):
        if self.lock.locked():
            print(f"{self.owner} 🔓 {self.name}")
            self.owner = None
            self.lock.release()

resources = {
    "printer": Resource("🖨️"),
    "disk": Resource("💾"),
}

def worker(name, needed_resources):
    for res in needed_resources:
        resources[res].acquire(name)
        time.sleep(1)
    print(f"{name}: ✅")
    for res in needed_resources:
        resources[res].release()

if __name__ == "__main__":
    thread1 = threading.Thread(target=worker, args=("A", ["printer", "disk"]))
    thread2 = threading.Thread(target=worker, args=("B", ["disk", "printer"]))
    thread1.start()
    thread2.start()
    thread1.join() 
    thread2.join()
