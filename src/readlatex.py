
from os import makedirs, chdir, system
from os.path import exists, basename, dirname, abspath
from shutil import copyfile, rmtree
from sys import argv

script_location = abspath(argv[0])

def readlatex(path):
    print("Compiling %s" % path)
    rmtree('out')
    chdir(dirname(dirname(script_location)))
    create_if_not_exists('out')
    copyfile('src/readlatex.sty', 'out/readlatex.sty')
    copyfile(path, 'out/' + basename(path))
    chdir('out')
    # make sure pdf output has correct references
    for _ in range(3):
        system('pdflatex ' + basename(path))
    

def create_if_not_exists(directory):
    if not exists(directory):
        makedirs(directory)

readlatex(argv[1])