from os.path import splitext

def heights_path(path):
    return splitext(path)[0] + ".readlatex_heights"

def locations_path(path):
    return splitext(path)[0] + ".readlatex_locations"

def pageheight_path(path):
    return splitext(path)[0] + ".readlatex_pageheight"

def output_path(path):
    return splitext(path)[0] + ".readlatex_output"
