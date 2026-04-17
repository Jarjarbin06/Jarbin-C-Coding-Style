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
name = f"{category}3"
info = f"""
{language}-{name} - File coherence
A source file must match a logical entity, and group all the functions associated with that entity.
Grouping functions that are not related to each other in the same file has to be avoided.
You are allowed to have 10 functions (including at most 5 non-static functions) in total per file.
"""
level = 2

# Imports #
import re
import jarbin_toolkit_console as Console

from utils.error import RuleError

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #
VAR_CHECKED_EXTENSIONS = "c"
VAR_CHECKED_EXTENSIONS_doc = "List of file extensions analyzed for function coherence."
VAR_INCLUDED_FOLDERS = "sources"
VAR_INCLUDED_FOLDERS_doc = "List of folders where files are checked by this rule."

# Regex #
RE_INCLUDED_PATTERN = None
RE_EXTENSION_PATTERN = re.compile(r'\.([^.\/]+)$')
RE_AUTHORIZED_PATTERN = None
RE_FUNCTION_PATTERN = None

# Checker #
def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    global VAR_CHECKED_EXTENSIONS, VAR_INCLUDED_FOLDERS
    VAR_CHECKED_EXTENSIONS = kwargs.get("VAR_CHECKED_EXTENSIONS", VAR_CHECKED_EXTENSIONS)
    VAR_INCLUDED_FOLDERS = kwargs.get("VAR_INCLUDED_FOLDERS", VAR_INCLUDED_FOLDERS)

    if isinstance(VAR_CHECKED_EXTENSIONS, tuple):
        VAR_CHECKED_EXTENSIONS = VAR_CHECKED_EXTENSIONS[0]
    if isinstance(VAR_INCLUDED_FOLDERS, tuple):
        VAR_INCLUDED_FOLDERS = VAR_INCLUDED_FOLDERS[0]

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: variables set").debug()
        )

    # Regex re-compiling #
    global RE_INCLUDED_PATTERN, RE_AUTHORIZED_PATTERN, RE_FUNCTION_PATTERN
    RE_INCLUDED_PATTERN = re.compile(
        rf"(?:^|/)(?:{'|'.join(map(re.escape, VAR_INCLUDED_FOLDERS.split()))})(?:/)",
        re.IGNORECASE
    )
    RE_AUTHORIZED_PATTERN = re.compile(
        rf"^({'|'.join(map(re.escape, VAR_CHECKED_EXTENSIONS.split()))})$",
        re.IGNORECASE
    )
    RE_FUNCTION_PATTERN = re.compile(
        r'^\s*(static\s+)?[a-zA-Z_][\w\s\*]*\s+[a-zA-Z_]\w*\s*\([^;]*\)\s*\{',
        re.MULTILINE
    )

    # Custom check #
    def check_file_coherence(file: str) -> bool:

        if not RE_INCLUDED_PATTERN.search(file):
            if verbose == 2:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} not in VAR_INCLUDED_FOLDERS").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        match = RE_EXTENSION_PATTERN.search(file)
        if not match:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} no extension to check").debug(),
                    Text("(skip)").valid().italic()
                )
            return True

        file_ext = match.group(1)
        if not RE_AUTHORIZED_PATTERN.match(file_ext):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} extension not checked").debug(),
                    Text("(skip)").valid().italic()
                )
            return True

        if not file_ext.lower() in VAR_CHECKED_EXTENSIONS:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} extension not checked").debug(),
                    Text("(skip)").valid().italic()
                )
            return True

        try:
            with open(file, "r") as f:
                content = f.read()
        except Exception:
            return True

        functions = RE_FUNCTION_PATTERN.findall(content)
        total_functions = len(functions)
        non_static_functions = sum(1 for f in functions if not f)

        if total_functions > 10 or non_static_functions > 5:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} too many functions").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} file valid").debug(),
                Text("(skip)").valid().italic()
            )
        return True

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: starting check").debug()
        )

    # Main loop #
    for file in paths:
        try:
            assert check_file_coherence(file), (
                f"{file}\n"
                "A source file must not exceed 10 functions "
                "(with at most 5 non-static functions)"
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
