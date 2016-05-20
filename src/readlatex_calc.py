
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
    @property
    def height(self):
        return self.__height

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

    def fig_height(self, ref):
        return self.__figures[ref.label].height

    def total_fig_height(self, values):
        return sum(self.fig_height(ref) for ref in values)

class Reference:
    def __init__(self, params, label, index, position):
        self.__params = params
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

    def same_figure(self, other):
        return self.__label == other.__label

    def distance(self, other):
        return abs(self.__position - other.__position)

    def removability(self, figs, otherrefs):
        unweighted = self.__params.penalty_height
        for other in otherrefs:
            if self == other:
                continue
            term = 1 / (self.distance(other) + 1)
            if self.same_figure(other):
                term *= self.__params.penalty_duplication + 1
            unweighted += term
        return figs.fig_height(self) * unweighted

    @property
    def label(self):
        return self.__label

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, pos):
        self.__position = pos

class Page:
    def __init__(self, params, pagenumber, height):
        self.__params = params
        self.__refs = []
        self.__pagenumber = pagenumber
        self.__height = height

    def resolve(self, figs):
        self.remove_extras(figs)
        resolver = self.__resolver(figs)
        for _ in range(self.__params.resolution_iterations):
            resolver.iterate()
        self.__apply(resolver)

    def remove_extras(self, figs):
        refs_with_removability = sorted(self.__refs, key=lambda ref: ref.removability(figs, self.__refs))
        fig_height = figs.total_fig_height(refs_with_removability)
        while fig_height > self.__height:
            ref = refs_with_removability.pop()
            fig_height -= figs.fig_height(ref)
        self.__refs = sorted(refs_with_removability)

    def __resolver(self, figs):
        return PageResolver(self.__params, self.__height, self.__refs, figs)

    def __apply(self, resolver):
        for i in range(resolver.n):
            self.__refs[i].position = resolver.ys[i]

    def add(self, label, index, position):
        if not isinstance(position, float):
            raise RuntimeError("The position should be of type float, but is of type %s" % type(position))
        ref = Reference(self.__params, label, index, position)
        self.__refs.append(ref)
        self.__refs.sort()

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class PageResolver:
    def __init__(self, params, height, refs, figs):
        self.params = params
        self.refs = refs
        self.height = height
        self.n = len(refs)
        self.figs = figs
        total_gap = height - figs.total_fig_height(refs)
        self.gap = total_gap / (self.n + 1)
        self.evenly_layout_ys()

    def evenly_layout_ys(self):
        self.ys = [self.gap]
        for i in range(1, self.n):
            self.ys.append(self.y(i - 1) + self.gap + self.h(i-1))
        for i in range(self.n):
            self.ys[i] += self.h(i) / 2

    def iterate(self):
        def mobile_proportion(i):
            """the proportion that the reference at i can move"""
            return abs(self.potential_movement(i)) / abs(self.y(i) - self.pos(i))
        best_i = max(range(self.n), key=mobile_proportion)
        self.ys[best_i] += self.potential_movement(best_i)

    def potential_movement(self, i):
        from math import copysign
        delta = self.y(i) - self.pos(i)
        direction = -int(copysign(1, delta)) # negative because we want to go the other way
        distance = self.y(i + direction) - self.y(i)
        amount_of_space_figures_take = self.h(i) / 2 + self.h(i + direction) / 2
        gapsize = copysign(abs(distance) - amount_of_space_figures_take, distance)
        gapsize *= self.params.resolution_narrowing
        if abs(gapsize) > abs(delta):
            # ensure that we don't overshoot
            gapsize = delta
        return gapsize

    def y(self, i):
        if i == -1:
            return 0
        if i == self.n:
            return self.height
        return self.ys[i]

    def pos(self, i):
        return self.refs[i].position

    def h(self, i):
        if i == -1 or i == self.n:
            return 0
        return self.figs.fig_height(self.refs[i])


def get_pages(params, locations, page_height):
    pages = {}
    index = 0
    for name, page, loc in read_by_ns(3, locations):
        page = int(page)
        if page not in pages:
            pages[page] = Page(params, page, page_height)
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