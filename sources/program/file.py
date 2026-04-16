#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from os import walk
from os.path import normpath, abspath, isdir, join as path_join

def get_files(
        root: str = "./",
        excludes: list[str] | None = None,
    ) -> list[str] | None:

    if not isdir(root):
        return None

    files: list[str] = []
    root = normpath(abspath(root))
    excludes = excludes or []

    for current_root, dirs, filenames in walk(root):

        dirs[:] = [
            d for d in dirs
            if d not in excludes and not d.startswith(".")
        ]

        for filename in filenames:
            if filename.startswith("."):
                continue

            files.append(normpath(path_join(current_root, filename)))

    return files
