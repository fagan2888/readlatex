
def positioning(path):
    figs = Figures.read(heights_path(path))
    pages = get_pages(locations_path(path))
    resolved = []
    for page in pages:
        resolved.append(page.resolve(figs))
    write_fig_positions(resolved)

class Figure:
    def __init__(self, name, height):
        self.__name = name
        self.__height = height

class Figures:
    def get(path):
        figures = {}
        for name, y0, yf in read_by_ns(3, path):
            name = name.strip("readlatex@savedfigcontent:")
            y = latex_pt_to_float(yf) - latex_pt_to_float(y0)
            figures[name] = Figure(name, y)
        return Figures(figures)

    def __init__(self, figures):
        self.__figures = figures

    def filter(pred):
        return Figures({k:v for k, v in self.__figures.items() if pred(k)})

class Reference:
    def __init__(self, label, index, position):
        self.__label = label
        self.__index = index
        self.__position = position

    def __eq__(self, other):
        return not self < other and not self > other

    def __lt__(self, other):
        if self.__position != other.__position:
            return self.__position < other.__position
        return self.__index < other.__index
    def __repr__(self):
        return repr(self.__dict__)

class Page:
    def __init__(self, pagenumber, height):
        self.__refs = []
        self.__pagenumber = pagenumber
        self.__height = height

    def resolve(self, figs):
        pass

    def add(self, label, index, position):
        if not isinstance(position, float):
            raise RuntimeError("The position should be of type float, but is of type %s" % type(position))
        ref = Reference(label, index, position)
        self.__refs.append(ref)
        self.__refs.sort()

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def get_pages(locations, page_height):
    pages = {}
    index = 0
    for name, page, loc in read_by_ns(3, locations):
        page = int(page)
        if page not in pages:
            pages[page] = Page(page, page_height)
        pages[page].add(name, index, latex_pt_to_float(loc))
        index += 1
    return pages

def read_by_ns(n, path):
    with open(path) as f:
        lines = [line.strip("\n") for line in f.readlines()]
        if len(lines) % n != 0:
            raise RuntimeError("Bad format for the heights file %r; length should be divisible by 3" % path)
        for i in range(len(lines) // n):
            yield tuple(lines[i * n : (i + 1) * n])

def latex_pt_to_float(val):
    return float(val.strip("pt"))