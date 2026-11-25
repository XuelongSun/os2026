import random, time
from memory import FixedMemory, DynamicMemory
from colorama import init, Fore, Back, Style

# Initialize colorama for Windows compatibility
init(autoreset=True)

def visualize_memory(memory:FixedMemory | DynamicMemory):
    print("┌" , end='')
    for i, b in enumerate(memory.blocks):
        if i == len(memory.blocks) - 1:
            print("─" * (b.length) + "┐")
        else:
            print("─" * (b.length) + "┬", end='')
    print("│" , end='')
    for b in memory.blocks:
        # Visual representation of each block as 
        # | 2KB | p1: 2KB|
        if b.free:
            block_display = Fore.GREEN + f"{b.length}".center(b.length, ' ') + Style.RESET_ALL + "│" 
        else:
            block_display = Back.RED + Fore.WHITE + f"{b.name}:{b.length}".center(b.length, ' ') + Style.RESET_ALL + "│"

        print(block_display, end='')
    print()
    print("└" , end='')
    for i, b in enumerate(memory.blocks):
        if i == len(memory.blocks) - 1:
            print("─" * (b.length) + "┘")
        else:
            print("─" * (b.length) + "┴", end='')
    
def generate_requests(time_duration=[2, 10], size_range=[6, 25], prob=0.7):
    global requests
    if random.random() > prob:
        return None
    time_d = random.randint(time_duration[0], time_duration[1])
    size = random.randint(size_range[0], size_range[1])
    request = {
        'name': f"P{len(requests)+1}",
        'time_duration': time_d,
        'size': size
    }
    return request

def run(memory:FixedMemory | DynamicMemory):
    global requests, clock, failed_num
    # first deallocate finished requests
    for req in requests:
        if 'end_time' in req and clock >= req['end_time']:
            success = memory.deallocate(req['start_addr'])
            if success:
                print(f"[Time {clock}]: {req['name']} done.")
                visualize_memory(memory)
                # remove end_time and start_addr to avoid repeated deallocation
                del req['end_time']
                del req['start_addr']
            else:
                print(f"[Time {clock}]: Failed to deallocate {req['name']}.")
    # then generate new requests
    request = generate_requests()
    # you can also manually create a request for testing: 
    # request = {'name': f'P{len(requests)+1}', 'time_duration': 5, 'size': 20}
    if request is not None:
        requests.append(request)
        start = memory.allocate(request['name'], request['size'])
        if start is not None:
            request['start_addr'] = start
            request['end_time'] = clock + request['time_duration']
            print(f"[Time {clock}]: {request['name']} requests {request['size']}KB [t={request['time_duration']},addr={start}].")
            visualize_memory(memory)
        else:
            print(f"[Time {clock}]: Failed to allocate {request['name']} of size {request['size']}KB.")
            failed_num += 1
            requests.remove(request)

    clock += 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        mem_type = sys.argv[1]
        if mem_type == "fixed":
            block_size = sys.argv[2]
            if block_size.isdigit():
                block_size = int(block_size)
                memory = FixedMemory(size=100, block_size=block_size)
            else:
                block_size = list(map(int, block_size.split(',')))
                memory = FixedMemory(size=sum(block_size), block_size=block_size)
        elif mem_type == "dynamic":
            policy = "first-fit"
            if len(sys.argv) >= 3:
                policy = sys.argv[2]
            else:
                print("No policy specified for dynamic memory, using first-fit by default.")
            memory = DynamicMemory(size=100, policy=policy)
    else:
        print("No memory type specified, using dynamic memory with first-fit policy by default.")
        memory = DynamicMemory(size=100,policy="first-fit")
    requests = []
    clock = 0
    failed_num = 0
    
    # let user use keyboard to step simulation
    while True:
        key = input(">")
        if key.lower() == 'q':
            break
        elif key == '':
            result = run(memory)
        elif key.lower() == 'a':
            # auto run
            times = input("Press type the time to run...")
            if times.isdigit():
                times = int(times)
            else:
                print("Invalid input, run 10 times by default.")
                times = 10
            while times > 0:
                result = run(memory)
                time.sleep(0.5)
                times -= 1
        elif key.lower() == 'r':
            # reset memory
            memory.reset()
            clock = 0
            requests = []
            print("Reset.")
        else:
            print("Invalid input. Press Enter to step, 'a' to auto run, 'r' to reset, 'q' to quit.")
    
    print(f"Simulation ended. Total failed requests: {failed_num}")
