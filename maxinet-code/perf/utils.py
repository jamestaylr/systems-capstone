def parse_ping_results(output):
    for line in output.splitlines():
        for t in [s for s in line.split() if 'time=' in s]:
            time = float(t.split('=')[-1])
            times.append(time)
    return sum(times) / len(times)
