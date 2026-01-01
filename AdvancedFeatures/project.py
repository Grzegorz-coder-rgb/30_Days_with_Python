import time

def read_logs(path):
    assert path.endswith(".log"), "File must be .log"
    with open(path) as f:
        for line in f:
            yield line.strip()

def filter_errors(lines):
    return filter(lambda l: "ERROR" in l, lines)

def format_lines(lines):
    return map(lambda l: l.upper(), lines)

def sort_lines(lines):
    return sorted(lines)

def analyze(path, *keywords):
    start = time.perf_counter()

    lines = read_logs(path)

    if keywords:
        lines = filter(
            lambda l: any(k in l for k in keywords),
            lines
        )

    lines = format_lines(lines)
    lines = sort_lines(lines)

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    print("Time:", time.perf_counter() - start)

analyze("logger.log", "ERROR")



