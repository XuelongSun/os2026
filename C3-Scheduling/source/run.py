from scheduler import Process, FCFS, SJF, HRRNp, RR, SRTF, MLFQ
from scheduler import RTProcess, EDF, LLF
from analyser import calculate_metrics, print_metrics, plot_gantt

if __name__ == "__main__":
    processes = [
        Process("A",0,5),
        Process("B",1,3),
        Process("C",2,4),
        # Process("P3",4,2),
    ]
    rt_process = [
        RTProcess("T1",0,3,7),
        RTProcess("T2",1,2,6),
        RTProcess("T3",2,2,5),
    ]
    # scheduler = LLF(rt_process)
    scheduler = RR(processes,quantum=3)
    scheduler.run()
    print(scheduler)
    print_metrics(calculate_metrics(scheduler.process, scheduler.segments))
    plot_gantt(scheduler.process, scheduler.segments, scheduler.name)
