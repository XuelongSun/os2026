#!/usr/bin/env python3

import sys
import json
import argparse
from collections import defaultdict
import matplotlib.pyplot as plt

# ============================================================
# Metrics
# ============================================================

def calculate_metrics(
    processes,
    segments
):

    first_start = {}
    completion = {}

    for s in segments:

        name = s["name"]

        if name not in first_start:
            first_start[name] = s["start"]

        completion[name] = s["end"]

    metrics = []

    for p in processes:

        name = p["name"]

        arrival = p["arrive_time"]

        service = p["service_time"]

        finish = completion[name]

        turnaround = (
            finish - arrival
        )

        waiting = (
            turnaround - service
        )

        response = (
            first_start[name]
            - arrival
        )

        metrics.append({
            "name": name,
            "arrival": arrival,
            "service": service,
            "finish": finish,
            "turnaround": turnaround,
            "waiting": waiting,
            "response": response
        })

    return metrics


# ============================================================
# Print metrics
# ============================================================

def print_metrics(
    data,
    metrics
):

    algorithm = data["algorithm"]

    print()

    print(
        f"===== {algorithm} Scheduling ====="
    )

    if algorithm == "RR":

        print(
            f"Time quantum = "
            f"{data['quantum']:g}"
        )

    print()

    header = (
        f"{'Process':<10}"
        f"{'Arrival':>10}"
        f"{'Service':>10}"
        f"{'Finish':>10}"
        f"{'Turnaround':>12}"
        f"{'Waiting':>10}"
        f"{'Response':>10}"
    )

    print(header)

    print(
        "-" * len(header)
    )

    for m in metrics:

        print(
            f"{m['name']:<10}"
            f"{m['arrival']:>10g}"
            f"{m['service']:>10g}"
            f"{m['finish']:>10g}"
            f"{m['turnaround']:>12g}"
            f"{m['waiting']:>10g}"
            f"{m['response']:>10g}"
        )

    print(
        "-" * len(header)
    )

    n = len(metrics)

    avg_turnaround = sum(
        x["turnaround"]
        for x in metrics
    ) / n

    avg_waiting = sum(
        x["waiting"]
        for x in metrics
    ) / n

    avg_response = sum(
        x["response"]
        for x in metrics
    ) / n

    print(
        f"{'Average':<40}"
        f"{avg_turnaround:>12.2f}"
        f"{avg_waiting:>10.2f}"
        f"{avg_response:>10.2f}"
    )

    print()


# ============================================================
# Gantt
# ============================================================

def plot_gantt(data):

    colors = ('bisque','lavender','mistyrose','honeydew')
    processes = data[
        "processes"
    ]

    segments = data[
        "segments"
    ]

    algorithm = data[
        "algorithm"
    ]
    
    title = algorithm

    if algorithm == "RR":

        title += (
            f" (q={data['quantum']:g})"
        )

    # -------------------------------------------
    # Arrival events
    # -------------------------------------------

    arrivals = defaultdict(list)

    for p in processes:

        arrivals[
            p["arrive_time"]
        ].append(
            p["name"]
        )


    # -------------------------------------------
    # Figure
    # -------------------------------------------

    fig, (
        ax_arrival,
        ax_cpu
    ) = plt.subplots(
        2,
        1,
        sharex=True,
        figsize=(
            11,
            2 + 0.65 * len(processes)
        ),
        gridspec_kw={
            "height_ratios": [
                1,
                max(
                    2,
                    len(processes)
                )
            ]
        }
    )

    # ========================================================
    # Arrival
    # ========================================================

    for i, (t, names) in enumerate(sorted(
        arrivals.items())
    ):

        ax_arrival.vlines(
            t,
            0,
            0.45,
            color=colors[i%len(colors)]
        )

        ax_arrival.scatter(
            [t],
            [0.45],
            marker="v",
            color=colors[i%len(colors)]
        )

        ax_arrival.text(
            t,
            0.58,
            ", ".join(names),
            ha="center",
            va="bottom",
            fontsize=10
        )

        # 到达时间也直接标出来
        ax_arrival.text(
            t,
            0.05,
            f"$t_a={t:g}$",
            ha="center",
            va="bottom",
            fontsize=10
        )

    ax_arrival.set_ylim(
        0,
        1
    )

    ax_arrival.set_yticks([])

    ax_arrival.set_ylabel(
        "Arrival",
    )
    ax_arrival.yaxis.set_label_coords(-0.03,0.5)
    ax_arrival.set_title(
        f"{title} Scheduling"
    )

    ax_arrival.spines[
        "left"
    ].set_visible(False)

    ax_arrival.spines[
        "right"
    ].set_visible(False)

    ax_arrival.spines[
        "top"
    ].set_visible(False)

    # ========================================================
    # CPU execution
    # ========================================================

    by_process = defaultdict(list)

    for s in segments:

        by_process[
            s["name"]
        ].append(
            (
                s["start"],
                s["end"] - s["start"]
            )
        )

    y_position = {
        p["name"]: i
        for i, p in enumerate(processes)
    }

    for i, p in enumerate(processes):

        name = p["name"]

        y = y_position[name]

        intervals = (
            by_process[name]
        )

        for start, width in intervals:
            ax_cpu.text(
                start + width / 2,
                y,
                f"{name} ($t_s={int(p['service_time']):d}$)",
                ha="center",
                va="center",
                fontsize=10
            )
            
            ax_cpu.barh(
                y, width, height=0.76, align='center', left=start,
                color=colors[i%len(colors)]
            )

    ax_cpu.set_yticks(
        range(
            len(processes)
        ),
        [
            p["name"]
            for p in processes
        ]
    )

    ax_cpu.set_ylim(
        -0.7,
        len(processes) - 0.3
    )

    ax_cpu.invert_yaxis()

    ax_cpu.set_ylabel(
        "CPU"
    )

    ax_cpu.set_xlabel(
        "Time"
    )

    max_t = int(sum([p["service_time"] for p in processes]))
    ax_cpu.set_xticks(range(max_t+1))
    
    ax_cpu.grid(
        axis="x",
        alpha=0.25
    )

    plt.tight_layout()
    plt.show()


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Analyse scheduling result"
        )
    )

    parser.parse_args()

    try:

        # 从 scheduler.py 接收 JSON
        data = json.load(
            sys.stdin
        )

        metrics = (
            calculate_metrics(
                data["processes"],
                data["segments"]
            )
        )

        # 先打印
        print_metrics(
            data,
            metrics
        )

        # # 再画图
        plot_gantt(
            data
        )

    except Exception as e:

        print(
            f"analyser.py: {e}",
            file=sys.stderr
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
