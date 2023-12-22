"""Copy figures used by document."""
import os
import os.path
import shutil
import errno
import tempfile
from pathlib import PurePath

dirpath = tempfile.mkdtemp()  # use a tempdir if outputdir not specified

cwd = os.getcwd()

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
        print(image[0])
        print(image[1])
        shutil.copy2(image[0], 'compiled')


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
    image_files = get_image_files()
    file_list = []
    manifest = ["# File list"]
    MAIN_PDF = DEP_FILE_BASE + ".pdf"
    file_list.append(MAIN_PDF)
    manifest.append(f'- {MAIN_PDF}:\t compiled master pdf')
    file_list.append(MAIN_FILE)
    manifest.append(f'- {MAIN_FILE}:\t master tex file')
    file_list.append(BIB_FILE)
    manifest.append(f'- {BIB_FILE}:\t bib entries file')
    for i, file_name in enumerate(image_files):
        manifest.append(f'- {file_name}:\t Figure {i+1}')
        file_list.append(file_name)
    input_files = get_input_files()
    for i, file_name in enumerate(input_files):
        manifest.append(f'- {file_name}:\t Input tex file')
        file_list.append(file_name)
    print("\n".join(manifest))
    print(file_list)

    # create manifest directory (if it doesnt exist)
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # copy files over to manifest directory
    for file_name in file_list:
        dest = os.path.join(TARGET_DIR, file_name)
        path = os.path.dirname(dest)
        make_sure_path_exists(path)
        shutil.copyfile(file_name, dest)
        print(f"{file_name} not added.")

    # write manifest list as README.md
    with open(os.path.join(TARGET_DIR, 'README.md'), 'w') as readme:
        readme.write("\n".join(manifest))

    # create archive
    shutil.make_archive(DEP_FILE_BASE, 'zip', TARGET_DIR)

    if TMP_FLAG:
        shutil.rmtree(dirpath)


