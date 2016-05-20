from os.path import splitext

def heights_path(path):
    return splitext(path)[0] + ".readlatex_heights"

def locations_path(path):
    return splitext(path)[0] + ".readlatex_locations"