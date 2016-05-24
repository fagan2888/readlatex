from readlatex_paths import *
from readlatex_calc import *

HEADER_CRUFT = "readlatex@savedfigcontent:"

def positioning(params, path):
    figs = read_figures(heights_path(path))
    pages = get_pages(params, locations_path(path), read_page_height(pageheight_path(path)))
    for page in pages:
        page.resolve(figs)
    write_fig_positions(output_path(path), pages, figs)

def get_pages(params, locations, page_height):
    pages = {}
    index = 0
    for name, page, loc in read_by_ns(3, locations):
        page = int(page)
        if page not in pages:
            pages[page] = Page(params, page, page_height)
        pages[page].add(name, index, latex_pt_to_float(loc))
        index += 1
    return list(pages.values())

def read_page_height(path):
    with open(path) as f:
        return latex_pt_to_float(f.read().strip("\n"))

def read_figures(path):
    figures = {}
    for name, y0, yf in read_by_ns(3, path):
        if not name.startswith(HEADER_CRUFT):
            raise AssertionError("Malformatted name, no header cruft: " + name)
        name = name[len(HEADER_CRUFT):]
        y = latex_pt_to_float(yf) - latex_pt_to_float(y0)
        figures[name] = Figure(name, y)
    print(figures)
    return Figures(figures)

def write_fig_positions(path, pages, figs):
    with open(path, "w") as f:
        for page in pages:
            for ref in page:
                pos = ref.position - figs.fig_height(ref) / 2
                f.write(r"\reusefigure{%s}{%spt}{%s}%s" % (page.number, pos, ref.label, "\n"))
