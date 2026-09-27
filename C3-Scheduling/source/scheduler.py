import sys
import argparse
import re
import json
from dataclasses import dataclass, asdict
from collections import deque

EPS = 1e-12

@dataclass
class Process:
    name: str
    arrive_time: float
    service_time: float

@dataclass
class Segment:
    name: str
    start: float
    end: float
    
def parse_processes(text):
    pattern = re.compile(
        r"""\(
            \s*["']([^"']+)["']\s*,
            \s*(-?\d+(?:\.\d+)?)\s*,
            \s*(-?\d+(?:\.\d+)?)\s*
            \)
        """,
        re.VERBOSE
    )
    processes = []
    
    for match in pattern.finditer(text):

        name = match.group(1)
        arrive = float(match.group(2))
        service = float(match.group(3))

        if arrive < 0:
            raise ValueError(
                f"{name}: arrive_time must be >= 0"
            )

        if service <= 0:
            raise ValueError(
                f"{name}: service_time must be > 0"
            )

        processes.append(
            Process(
                name,
                arrive,
                service
            )
        )

    if not processes:
        raise ValueError(
            "No valid Process(...) found in stdin."
        )

    names = [p.name for p in processes]

    if len(names) != len(set(names)):
        raise ValueError(
            "Process names must be unique."
        )

    return processes

def append_segment(segments, name, start, end):

    if end <= start + EPS:
        return

    # 连续运行的同一进程自动合并
    if (
        segments
        and segments[-1].name == name
        and abs(segments[-1].end - start) < EPS
    ):
        segments[-1].end = end

    else:
        segments.append(
            Segment(name, start, end)
        )

def rr(processes, quantum):

    if quantum <= 0:
        raise ValueError(
            "quantum must be > 0"
        )

    n = len(processes)

    order = sorted(
        enumerate(processes),
        key=lambda x: (
            x[1].arrive_time,
            x[0]
        )
    )

    remaining = {
        i: p.service_time
        for i, p in enumerate(processes)
    }

    ready = deque()

    segments = []

    k = 0

    t = order[0][1].arrive_time

    def add_arrivals(now):

        nonlocal k

        while (
            k < n
            and order[k][1].arrive_time
            <= now + EPS
        ):

            i, _ = order[k]

            ready.append(i)

            k += 1

    add_arrivals(t)

    while ready or k < n:

        if not ready:

            t = max(
                t,
                order[k][1].arrive_time
            )

            add_arrivals(t)

        i = ready.popleft()

        p = processes[i]

        run_time = min(
            quantum,
            remaining[i]
        )

        end = (
            t + run_time
        )

        append_segment(
            segments,
            p.name,
            t,
            end
        )

        remaining[i] -= run_time

        t = end

        # 时间片内到达的新进程
        # 先进入 ready queue
        add_arrivals(t)

        # 当前进程未结束
        # 放回队尾
        if remaining[i] > EPS:
            ready.append(i)

    return segments

def main():
    parser = argparse.ArgumentParser(
        description="CPU scheduling simulator"
    )
    
    parser.add_argument(
        "algorithm",
        choices=[
            "FCFS",
            "SJF",
            "HRRN",
            "SRTF",
            "RR"
        ]
    )
    
    parser.add_argument(
        "-q",
        "--quantum",
        type=float,
        default=2.0,
        help="time quantum for RR"
    )
    
    args = parser.parse_args()

 

    # stdin
    text = sys.stdin.read()
    processes = parse_processes(
        text
    )

    if args.algorithm == "FCFS":
        segments = fcfs(processes)
        
    elif args.algorithm == "RR":
        segments = rr(
            processes,
            args.quantum
        )
    
    
    # Unix pipeline 的关键：
    # stdout 只输出机器可读 JSON
    result = {
        "algorithm":
            args.algorithm,

        "quantum":
            args.quantum
            if args.algorithm == "RR"
            else None,

        "processes": [
            asdict(p)
            for p in processes
        ],

        "segments": [
            asdict(s)
            for s in segments
        ]
    }

    json.dump(
        result,
        sys.stdout
    )

    
if __name__ == "__main__":
    main()
