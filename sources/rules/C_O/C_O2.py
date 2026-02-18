#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from Error import RuleError

AUTHORIZED_EXTENSIONS = "c h"
FOLDERS = "SOURCES INCLUDES"

def check(
        *args,
        **kwargs
    ) -> list[RuleError] | None:

    errors = []
    files_path : list[str] = args[0]
    auth_ext: str | None

    if "AUTHORIZED_EXTENSIONS" in kwargs :
        auth_ext = kwargs["AUTHORIZED_EXTENSIONS"]
    else :
        auth_ext = AUTHORIZED_EXTENSIONS

    if "FOLDER" in kwargs :
        folders = kwargs["FOLDERS"]
    else :
        folders = FOLDERS

    def check_file_ext(
            file : str
        ) -> bool:

        folder_check : bool = False

        for folder in folders :
            if folder in file.upper() :
                folder_check = True

        if not folder_check :
            return False

        file_ext : str = file.split("/")[-1]

        if "." in file_ext :
            file_ext = file_ext.split(".")[-1]
        else :
            return True

        if not file_ext in auth_ext.split(" ") :
            return False
        return True

    for file in files_path:
        try :
            assert check_file_ext(file), f"File {file} has an invalid extension"

        except AssertionError as error:
            errors.append(RuleError("C-O2", str(error)))

    return errors if errors else None
