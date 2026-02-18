#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from Error import RuleError

UNAUTHORIZED_EXTENSIONS = "o a so out gcda gcno gch pch swp swo tmp bak py"

def check(
        *args,
        **kwargs
    ) -> list[RuleError] | None:

    errors = []
    files_path : list[str] = args[0]
    unauth_ext: str | None

    if "UNAUTHORIZED_EXTENSIONS" in kwargs :
        unauth_ext = kwargs["UNAUTHORIZED_EXTENSIONS"]
    else :
        unauth_ext = UNAUTHORIZED_EXTENSIONS

    def check_file_ext(
            file : str
        ) -> bool:
        file_ext : str = file.split("/")[-1]

        if "." in file_ext :
            file_ext = file_ext.split(".")[-1]
        else :
            return True

        if file_ext in unauth_ext.split(" ") :
            return False
        return True

    for file in files_path:
        try :
            assert check_file_ext(file), f"File {file} has an invalid extension"

        except AssertionError as error:
            errors.append(RuleError("C-O1", str(error)))

    return errors if errors else None
