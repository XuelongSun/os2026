from dataclasses import dataclass

from analyser import segments_by_name, \
    show_name_segment, show_cpu_tick_axis


@dataclass
class Process:
    name: str
    arrive_time: int
    service_time: int
    priority: int=0

@dataclass
class RTProcess:
    name: str
    arrive_time: int
    service_time: int
    deadline: int
    
@dataclass
class Segment:
    name: str
    start: int
    end: int

class BaseScheduler:
    def __init__(self, processes:list[Process] | list[RTProcess], name="scheduler") -> None:
        self.process = processes
        self.name = name
        
        self.pending = sorted(self.process,
                              key=lambda x:x.arrive_time)
        self.ready = []
        self.t = 0
        
        self.last_owner = None
        self.current = None
        
        self.segments = []
        
    def admit(self):
        while self.pending and (self.pending[0].arrive_time <= self.t):
            self.ready.append(self.pending.pop(0))

    def append_segment(self, name, start, end):
        if end <= start:
            return

        # 连续运行的同一进程自动合并
        if (
            self.segments
            and self.segments[-1].name == name
            and abs(self.segments[-1].end - start) == 0
        ):
            self.segments[-1].end = end

        else:
            self.segments.append(
                Segment(name, start, end)
            )
    
    def sort_ready_queue(self):
        pass
        
    def run(self):
        self.admit()
        while self.ready or self.pending:
            if not self.ready:
                self.t = self.pending[0].arrive_time
                self.admit()
            self.sort_ready_queue()
            self.current = self.ready.pop(0)
            self.append_segment(self.current.name,
                                self.t,
                                self.t + self.current.service_time)
            self.t += self.current.service_time
            self.admit()
        
        return self.segments

        
    def __repr__(self) -> str:
        l = (self.t+2)*5 if self.t > 0 else 60
        string = "=" * l+ "\n"
        string += self.name + "\n"
        string += "=" *l + "\n"
        
        if self.segments:
            for n, ts in segments_by_name(self.segments).items():
                string += show_name_segment(n,
                                            [t[0] for t in ts],
                                            [t[1] for t in ts])
                string += "\n"
            string = show_cpu_tick_axis(string, self.t)
        else:
            return "call .run() to get scheduling results"
        return string
    

class FCFS(BaseScheduler):
    def __init__(
        self, processes: list[Process],
        name="First Come First Serve - FCFS") -> None:
        super().__init__(processes, name)
    
    def sort_ready_queue(self):
        self.ready.sort(key=lambda x: x.arrive_time)

    
class SJF(BaseScheduler):
    def __init__(
        self, processes: list[Process],
        name="Shortest Job First - SJF") -> None:
        super().__init__(processes, name)
        
    def sort_ready_queue(self):
        self.ready.sort(key=lambda x: x.service_time)


class HRRN(BaseScheduler):
    def __init__(
        self, processes: list[Process],
        name="Highest Response Ratio Next - HRRN") -> None:
        super().__init__(processes, name)
    
    def sort_ready_queue(self):
        self.ready.sort(key=lambda x: 1 + (self.t-x.arrive_time)/x.service_time, reverse=True)


class PreemptiveScheduler(BaseScheduler):
    def __init__(self, processes:list[Process] | list[RTProcess], name="preemptive scheduler") -> None:
        super().__init__(processes, name)
        self.wait_time = {p.name: 0 for p in self.process}
        self.remain_time = {p.name: p.service_time for p in self.process}
        self.last_owner = None
    
    def run(self):
        self.admit()
        while self.ready or self.pending:
            
            self.sort_ready_queue()
            self.current = self.ready[0]
            
            if self.last_owner is None:
                self.last_owner = self.current.name
            elif self.current.name != self.last_owner:
                self.last_owner = self.current.name
            
            for j in self.ready:
                if j.name != self.last_owner:
                    self.wait_time[j.name] += 1
            
            self.append_segment(self.current.name,
                                self.t,
                                self.t + 1)
            self.t += 1
            self.remain_time[self.current.name] -= 1
            if self.remain_time[self.current.name] == 0:
                self.ready.pop(0)
                
            self.admit()

        return self.segments

class HRRNp(PreemptiveScheduler):
    def __init__(
        self, processes: list[Process],
        name="Highest Response Ratio Next (preemptive) - HRRNp") -> None:
        super().__init__(processes, name)
        
    def sort_ready_queue(self):
        self.ready.sort(key=lambda x: 1 + self.wait_time[x.name]/self.remain_time[x.name],
                        reverse=True)


class SRTF(PreemptiveScheduler):
    def __init__(
        self, processes: list[Process], 
        name="Shortest Remaining Time First - SRTF") -> None:
        super().__init__(processes, name)
    
    def sort_ready_queue(self):
        self.ready.sort(key=lambda x: self.remain_time[x.name])


class RR(PreemptiveScheduler):
    def __init__(
        self, processes: list[Process],
        name="Round Robin - RR (q=2)",
        quantum=2) -> None:
        super().__init__(processes, name)
        self.q = quantum

    def run(self):
        self.admit()
        while self.ready or self.pending:
            self.current = self.ready.pop(0)
            
            if self.last_owner is None:
                self.last_owner = self.current.name
            elif self.current.name != self.last_owner:
                self.last_owner = self.current.name
            
            for j in self.ready:
                if j.name != self.last_owner:
                    self.wait_time[j.name] += 1
            
            rt = min(self.q, self.remain_time[self.current.name])
            self.append_segment(self.current.name,
                                self.t,
                                self.t + rt)
            self.t += rt
            self.remain_time[self.current.name] -= rt
            self.admit()
            if self.remain_time[self.current.name] > 0:
                self.ready.append(self.current)
        
        return self.segments
    

class MLFQ(PreemptiveScheduler):
    def __init__(
        self, processes: list[Process],
        name="Multi-Level Feedback Queue-MLFQ (q=[1,2])",
        quantum=[1, 2]) -> None:
        super().__init__(processes, name)
        self.Q = [[]] * len(quantum)
        self.Q[0] = self.ready
        self.quantum = quantum
        
    def run(self):
        self.admit()
        while self.pending or any(self.Q):
            for l, q in enumerate(self.quantum):
                if self.Q[l]:
                    self.current = self.Q[l].pop(0)
                    rt = min(q, self.remain_time[self.current.name])
                    self.append_segment(self.current.name,
                                        self.t,
                                        self.t + rt)
                    self.t += rt
                    self.remain_time[self.current.name] -= rt
                    self.admit()
                    # add to next level
                    if self.remain_time[self.current.name] > 0:
                        next_level = min([l+1, len(self.quantum)-1])
                        self.Q[next_level].append(self.current)
                        break
        return self.segments
    
    
class EDF(PreemptiveScheduler):
    def __init__(
        self, processes: list[RTProcess],
        name = "Earliest Deadline First - EDF"
    ):
        super().__init__(processes, name)
    
    def sort_ready_queue(self):
        self.ready.sort(key=lambda x: x.deadline)


class LLF(PreemptiveScheduler):
    def __init__(
        self, processes: list[RTProcess],
        name = "Least Laxity First - LLF"
    ):
        super().__init__(processes, name)
    
    def sort_ready_queue(self):
        self.ready.sort(
            key=lambda x: x.deadline - (self.t + self.remain_time[x.name])
        )
