"""Copy figures used by document."""
import os
import os.path
import shutil
import errno
import argparse
from pathlib import PurePath


description = 'Prepare single directory for submission'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('main', default='compiled', help="path to directory with dep and tex files", type=str)
#parser.add_argument("--outputdir", help="output directory for manifest",default="manifest")
parser.add_argument("--extensions", help="image file extensions",
                    default=['pdf', 'pdf_tex', 'png', 'jpg'])

args = parser.parse_args()

BASE_DIR = args.main
DEP_FILE = PurePath(BASE_DIR,'{{ cookiecutter.repo_name }}_generic.dep')
TEX_FILE =  PurePath(BASE_DIR,'{{ cookiecutter.repo_name }}_generic.tex')
EXTENSIONS = args.extensions


def get_input_files(DEP_FILE):
    r"""Check for \input files to add to Manifest."""
    files = []
    with open(DEP_FILE, 'r') as f:
        for line in f:
            print(line)
            if '*{file}' not in line:
                continue
            value = line.split('{')[2].split('}')
            source = value[0]
            _, e = os.path.splitext(source)
            if not e:
                source = source+".tex"
                files.append(source)
    return files


def get_image_files(DEP_FILE, EXTENSIONS=None):
    """Gather any image files for manifest."""
    if EXTENSIONS is None:
        EXTENSIONS = ['pdf', 'pdf_tex', 'png', 'jpg']
    img_files = []
    with open(DEP_FILE, 'r') as f:
        for line in f:
            print(line)
            if '*{file}' not in line:
                continue
            value = line.split('{')[2].split('}')
            source = value[0]
            _, e = os.path.splitext(source)
            e = e.lower()[1:]
            if e not in EXTENSIONS:
                continue
            print(source)
            img_files.append(source)
    return img_files

def strip_path(images):
    images = [PurePath(i) for i in images]
    return [PurePath(i.stem+i.suffix).as_posix() for i in images]
    

def copy_images(DEP_FILE, EXTENSIONS=None):
    imgs = get_image_files(DEP_FILE, EXTENSIONS)
    fns = strip_path(imgs)
    movers = zip(imgs, fns)
    for image in movers:
        print(image[1])
        shutil.copy2(image[0], BASE_DIR)


def rewrite_tex_file(tex_file, DEP_FILE, EXTENSIONS=None):
    imgs = get_image_files(DEP_FILE, EXTENSIONS)
    fns = strip_path(imgs)
    movers = zip(imgs, fns)

    with open(tex_file, 'r') as file: 
        data = file.read() 
        for i in movers:
            data = data.replace(i[0], i[1]) 
    with open(tex_file, 'w') as file: 
        file.write(data) 


def make_sure_path_exists(path):
    """Check for paths."""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def main():
    """Wrap application."""
    copy_images(DEP_FILE, EXTENSIONS)
    rewrite_tex_file(TEX_FILE, DEP_FILE, EXTENSIONS)


if __name__ == '__main__':
    main()