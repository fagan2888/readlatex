from readlatex_paths import *
from readlatex_calc import *

def positioning(path):
    figs = read_figures(heights_path(path))
    pages = get_pages(locations_path(path))
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
    return pages

def read_figures(path):
    figures = {}
    for name, y0, yf in read_by_ns(3, path):
        name = name.strip("readlatex@savedfigcontent:")
        y = latex_pt_to_float(yf) - latex_pt_to_float(y0)
        figures[name] = Figure(name, y)
    return Figures(figures)

def write_fig_positions(path, pages, figs):
    with open(path, "w") as f:
        for page in pages:
            for ref in page:
                f.write("readlatex@savedfigcontent:%s\n" % ref.label)
                f.write("%s\n" % page.number)
                pos = ref.location - figs.page_height(ref)
                f.write("%s\n" % pos)