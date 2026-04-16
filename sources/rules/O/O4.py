#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
language = "C"
category = "O"
name = f"{category}4"
info = f"""
{language}-{name} - Naming files and folders
The name of the file must define the logical entity it represents, and thus be clear, precise, explicit and
unambiguous.
All file names and folders must be in English, according to the snake_case convention (that is, only composed of lowercase, numbers, and underscores).
"""
level = "MINOR"

# Imports #
import re
import jarbin_toolkit_console as Console

from utils.error import RuleError

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #
ALLOWED_CHARS = r"^[a-z0-9_/\.]+$"
ALLOWED_CHARS_doc = "Regex pattern checking for invalid characters for files."
SNAKE_CASE = r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$"
SNAKE_CASE_doc = "Regex pattern enforcing snake_case naming convention for files and optional extensions."
GENERIC_NAMES = "algo file tmp temp misc stuff code"
GENERIC_NAMES_doc = "List of generic names to check."

# Regex #
RE_GENERIC_NAMES_PATTERN = None
RE_VALID_PATH_PATTERN = re.compile(ALLOWED_CHARS)
RE_SNAKE_CASE_PATTERN = re.compile(SNAKE_CASE)

# Checker #
def check(paths, **kwargs) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)
    root = kwargs.get("root", 0)

    global SNAKE_CASE, GENERIC_NAMES
    SNAKE_CASE = kwargs.get("SNAKE_CASE", SNAKE_CASE)
    GENERIC_NAMES = kwargs.get("GENERIC_NAMES", GENERIC_NAMES)

    if isinstance(SNAKE_CASE, tuple):
        SNAKE_CASE = SNAKE_CASE[0]
    if isinstance(GENERIC_NAMES, tuple):
        GENERIC_NAMES = GENERIC_NAMES[0]

    global RE_SNAKE_CASE_PATTERN, RE_GENERIC_NAMES_PATTERN
    RE_SNAKE_CASE_PATTERN = re.compile(SNAKE_CASE)

    RE_GENERIC_NAMES_PATTERN = re.compile(
        rf"^({'|'.join(map(re.escape, GENERIC_NAMES.split()))})$",
        re.IGNORECASE
    )

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: starting check").debug()
        )

    def check_file(file: str) -> bool:

        import os

        relative = os.path.relpath(file, root) if root else file
        parts = relative.split("/")
        file_name = parts[-1]
        folders = parts[:-1]

        for folder in folders:
            if folder and not RE_SNAKE_CASE_PATTERN.fullmatch(folder):
                if verbose:
                    print(
                        Text(" ").debug(title=True),
                        Text(f"C-{name}: {folder} is not snake_case").debug(),
                        Text("(invalid)").error().italic()
                    )
                return False

        name_no_ext = file_name.split(".")[0]

        if not RE_SNAKE_CASE_PATTERN.fullmatch(name_no_ext):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file_name} is not snake_case").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if RE_GENERIC_NAMES_PATTERN.search(name_no_ext):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file_name} is too generic").debug(),
                    Text("(warning)").warning().italic()
                )
            return False

        if verbose == 2:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {relative} valid").debug(),
                Text("(valid)").valid().italic()
            )
        return True

    # Main loop #
    for file in paths:
        try:
            assert check_file(file), (
                f"{file}\n"
                "File and folder names must follow snake_case and be explicit"
            )

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error), level=level))

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: ending check").debug(),
            Text(f"({len(errors)} errors found)").error().italic()
            if errors else Text("(no error)").valid().italic()
        )

    return errors if errors else None
