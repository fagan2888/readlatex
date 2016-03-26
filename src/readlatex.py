
from os import makedirs, chdir, system, remove
from os.path import exists, basename, dirname, abspath, join
from shutil import copyfile
from sys import argv

script_location = abspath(argv[0])

def readlatex(path):
    chdir(dirname(path))
    print("Compiling %s" % path)
    create_if_not_exists('out')
    location = join(dirname(script_location), 'readlatex.sty')
    copyfile(location, 'readlatex.sty')
    # make sure pdf output has correct references
    for _ in range(3):
        system('pdflatex ' + basename(path))
    remove('readlatex.sty')

def create_if_not_exists(directory):
    if not exists(directory):
        makedirs(directory)

readlatex(argv[1])