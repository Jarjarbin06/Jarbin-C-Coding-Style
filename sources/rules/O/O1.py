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
name = f"{category}1"
info = f"""
{language}-{name} - Contents of the repository
The repository must not contain compiled (.o, .a, .so, ...), temporary or unnecessary files (*~, #*#, etc.).
"""
level = "MAJOR"

# Imports #
import re
import jarbin_toolkit_console as Console

from utils.error import RuleError

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #
UNAUTHORIZED_EXTENSIONS = "o a so out gcda gcno gch pch swp swo tmp bak"
UNAUTHORIZED_EXTENSIONS_doc = "List of forbidden file extensions (compiled, temporary, or unnecessary files)."
EXCLUDED_FOLDERS = "bonus"
EXCLUDED_FOLDERS_doc = "List of folders excluded from the check (files inside are ignored)."

# Regex #
RE_EXCLUDED_PATTERN = None
RE_EXTENSION_PATTERN = re.compile(r'\.([^.\/]+)$')
RE_UNAUTHORIZED_PATTERN = None

# Checker #
def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    global UNAUTHORIZED_EXTENSIONS, EXCLUDED_FOLDERS
    UNAUTHORIZED_EXTENSIONS = kwargs.get("UNAUTHORIZED_EXTENSIONS", UNAUTHORIZED_EXTENSIONS)
    EXCLUDED_FOLDERS = kwargs.get("EXCLUDED_FOLDERS", EXCLUDED_FOLDERS)

    if isinstance(UNAUTHORIZED_EXTENSIONS, tuple):
        UNAUTHORIZED_EXTENSIONS = UNAUTHORIZED_EXTENSIONS[0]
    if isinstance(EXCLUDED_FOLDERS, tuple):
        EXCLUDED_FOLDERS = EXCLUDED_FOLDERS[0]

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: variables set").debug()
        )

    # Regex re-compiling #
    global RE_EXCLUDED_PATTERN, RE_UNAUTHORIZED_PATTERN
    RE_EXCLUDED_PATTERN = re.compile(
        rf"(?:^|/)(?:{'|'.join(map(re.escape, EXCLUDED_FOLDERS.split()))})(?:/)",
        re.IGNORECASE
    )
    RE_UNAUTHORIZED_PATTERN = re.compile(
        rf"^({'|'.join(map(re.escape, UNAUTHORIZED_EXTENSIONS.split()))})$",
        re.IGNORECASE
    )

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:

        match = RE_EXCLUDED_PATTERN.search(file)
        if match:
            folder = match.group(0).strip("/")
            if verbose == 2:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} in EXCLUDED_FOLDERS (\"{folder}\")").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        match = RE_EXTENSION_PATTERN.search(file)
        if not match:
            if verbose == 2:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} doesn't have an extension").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        file_ext = match.group(1)

        if RE_UNAUTHORIZED_PATTERN.match(file_ext):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} extension not allowed").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose == 2:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} extension allowed").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: starting check").debug()
        )

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), (
                f"{file}\n"
                f"The repository must not contain compiled (.o, .a, .so, ...), "
                f"temporary or unnecessary files (*~, #*#, etc.)"
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
