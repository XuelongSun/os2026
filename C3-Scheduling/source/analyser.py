from prettytable import PrettyTable
import matplotlib.pyplot as plt

def segments_by_name(segments):
    seg = {}
    for s in segments:
        if s.name in seg.keys():
            seg[s.name].append((s.start, s.end))
        else:
            seg.update({s.name:[(s.start, s.end)]})
    return seg

def calculate_metrics(processes, segments):
    seg_name = segments_by_name(segments)
    metrics = []
    for p in processes:
        name = p.name
        arrive = p.arrive_time
        service = p.service_time
        start = min([t[0] for t in seg_name[name]])
        complete = max([t[1] for t in seg_name[name]])
        
        turnaround = complete - arrive
        wait = turnaround - service
        response = start - arrive
        metrics.append(
            {
                'Process':name,
                'Arrival':arrive,
                'Start':start,
                'Finish':complete,
                'Turnaround': turnaround,
                'Waiting':wait,
                'Response':response
            }
        )
        if hasattr(p, 'deadline'):
            ok = '✓' if not complete > p.deadline else 'x'
            metrics[-1].update({'Deadline':ok})
            
    metrics.append(
        {
            'ProcessNum': len(processes),
            'Finish':max([m['Finish'] for m in metrics]),
            'Turnaround':sum([m['Turnaround'] for m in metrics])/len(processes),
            'Waiting':sum([m['Waiting'] for m in metrics])/len(processes),
            'Response':sum([m['Response'] for m in metrics])/len(processes),
        }
    )
    return metrics

def print_metrics(metrics):
    table = PrettyTable()
    
    table.field_names = metrics[0].keys()
    for m in metrics[:-1]:
        table.add_row(m.values())
    table.add_divider()
    row = [
        'Average'," ", " ", " ",
        metrics[-1]["Turnaround"],
        metrics[-1]["Waiting"],
        metrics[-1]["Response"],
    ]

    if 'Deadline' in metrics[0].keys():
        row += [' ']
        print(row)
    table.add_row(row)
    table.float_format = ".2f"

    print(table)
    
def show_name_segment(name, starts, ends):
    s = ''
    last_end = 0
    # upper
    for i, (start, end) in enumerate(zip(starts, ends)):
        width = (end - start) * 5
        if i == 0:
            s += "¦ "
        s += ' '*5*(start-last_end) + '+' + '-' * (width - 2) + '+'
        last_end = end
    
    s += "\n"
    last_end = 0
    for i, (start, end) in enumerate(zip(starts, ends)):
        width = (end - start) * 5
        padding_left = (width - len(name) - 2) // 2
        padding_right = width - padding_left - len(name) - 2
        if i == 0:
            s += "¦ "
        s += " "*5*(start-last_end) + "|" + " " * padding_left
        s += name
        s += " "*padding_right + "|"
        last_end = end
    
    s += "\n"
    last_end = 0
    for i, (start, end) in enumerate(zip(starts, ends)):
        width = (end - start) * 5
        if i == 0:
            s += "¦ "
        s += ' '*5*(start-last_end) + '+' + '-' * (width - 2) + '+'
        last_end = end

    return s

def show_cpu_tick_axis(s, length):
    
    for i in range(length + 1):
        # s += f"--{i}--"
        padding_left = (5 - len(str(i))) // 2
        padding_right = 5 - padding_left - len(str(i))
        s += "-" * padding_left + str(i) + "-"*padding_right
    s += "→\n"
    s += " " * (length*5 // 2) + " CPU Tick " + " " * (length*5 // 2)
    return s

def plot_gantt(processes, segments, title="scheduling"):
    colors = ('tomato','royalblue','darkorange','darkviolet','darkgreen')
    
    fig, (ax_arrival, ax_cpu) = plt.subplots(
        2, 1, sharex=True,
        figsize=(12, 2 + 0.8 * len(processes)),
        gridspec_kw={
            "height_ratios": [1, max(2, len(processes))]
        }
    )
    seg_name = segments_by_name(segments)
    max_te = 0
    for i, p in enumerate(processes):
        c = colors[i%len(colors)]
        ax_arrival.vlines(
            p.arrive_time, 0, 0.4, lw=2,
            color=c
        )
        ax_arrival.scatter(
            [p.arrive_time], [0.3], marker="d", color=c, s=120
        )
        ax_arrival.text(
            p.arrive_time, 0.45, p.name, 
            ha="center", va="bottom", fontsize=12,
            color=c
        )

        r = p.service_time
        for ts, te in seg_name[p.name]:
            w = te - ts
            if te > max_te:
                max_te = te
            ax_cpu.barh(
                i, w, left=ts,
                align="center", color=c, alpha=0.3
            )
            ax_cpu.text(
                ts + (w)/2, i, 
                f"{p.name} ($r={int(r-w):d}$)",
                ha="center", va="center",
                fontsize=12
            )
            r -= w
        
        if hasattr(p, 'deadline'):
            # add deadline for realtime process
            ax_cpu.vlines(
                p.deadline, -0.5, len(processes)+0.5,
                lw=2, ls='--', color=c
            )
            ax_cpu.text(
                p.deadline + 0.1, len(processes),
                p.name, rotation=45, va='bottom', color=c,
                fontsize=12
            )
            
    ax_arrival.set_title(f"{title}")
    ax_arrival.set_ylabel("Arrival")
    ax_arrival.set_yticks([])
    ax_arrival.set_ylim(0,0.8)
    ax_arrival.set_xlim(-0.1,max_te+0.1)
    
    for d in ["left", "right", "top"]:
        ax_arrival.spines[d].set_visible(False)

    # ax_arrival.yaxis.set_label_coords(-0.03,0.5)
    
    # 
    ax_cpu.set_yticks(
        range(len(processes)), [p.name for p in processes]
    )
    ax_cpu.set_ylim(-0.5, len(processes) - 0.5)
    
    ax_cpu.set_xlim(-0.1,max_te+1)
    ax_cpu.set_xlabel("CPU Tick")
    ax_cpu.set_xticks(range(max_te+1))
    ax_cpu.grid(axis="x", alpha=0.5)
    ax_cpu.invert_yaxis()    
    plt.tight_layout()
    plt.show()
    
    return fig, ax_arrival, ax_cpu

    