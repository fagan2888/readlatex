
def read_by_ns(n, path):
    with open(path) as f:
        lines = [line.strip("\n") for line in f.readlines()]
        if len(lines) % n != 0:
            raise RuntimeError("Bad format for the heights file %r; length should be divisible by 3" % path)
        for i in range(len(lines) // n):
            yield tuple(lines[i * n : (i + 1) * n])

def latex_pt_to_float(val):
    return float(val.strip("pt"))