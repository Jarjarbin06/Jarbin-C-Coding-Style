#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


# Program info #
__program__ = "JCCS (Jarbin-C-Coding-Style)"
__version__ : str = "v0.2"
__author__ : str = "Jarjarbin06"
__email__ : str = "nathan.amaraggi@epitech.eu"


# Program imports #
from os import listdir
from os.path import isfile as path_isfile, join as path_join
from sys import argv, stderr, exit
from typing import Callable, Any
from Error import RuleError
import jarbin_toolkit_console as Console
from rules.Rules import RULES

print = Console.Console.print
Text = Console.Text.Text
Color = Console.ANSI.Color
Cursor = Console.ANSI.Cursor

EXIT_SUCCESS = 0
EXIT_FAILURE = 84


# Program #
def show_arguments(
        rules: dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]]
    ) -> None:

    title = "   JCCS - RULES   "
    dash_title = "-" * (len(Console.Console) - len(title))
    dash = "-" * len(Console.Console)
    print(dash)
    print(dash_title[:int((len(Console.Console) - len(title)) / 2)] + title + dash_title[:int((len(Console.Console) - len(title)) / 2)])
    print(dash)

    last_rule = [rule for rule in rules][-1]

    for category in rules:

        print(Color(Color.C_BOLD) + dash_title[:int((len(Console.Console) - len(rules[category]["name"]) + 6) / 4)].replace("-", "=") + "   " + rules[category]["name"] + "   " + dash_title[:int((len(Console.Console) - len(rules[category]["name"]) + 6) / 4)].replace("-", "="))
        print(Color(Color.C_FG_DARK) + Text(rules[category]["info"]))

        for rule in rules[category]:
            if rule in ["name", "info"]:
                continue
            print(Text(rule).bold().underline())
            print(Color(Color.C_FG_DARK) + Text(rules[category][rule]["info"]), end="")
            print(Text("Arguments:"))
            if rules[category][rule]["arguments"] :
                for rule_arg in rules[category][rule]["arguments"]:
                    print("  - " + rule_arg + " : \"" + rules[category][rule]["arguments"][rule_arg] + "\"")

            else:
                print(Text("\t(no argument)").italic())

            if rule != last_rule:
                print("-" * len(Console.Console))

    print(dash)
    print(dash)

def missing_rule(
        *args,
        **kwargs
    )-> list[RuleError] | None:
    return [RuleError("Unknown Rule", "You tried to run an unknown rule")]

def get_files(
        root: str = "./",
    ) -> list[str]:

    files: list[str] = []

    try:
        root = (root if root[-1] == "/" else f"{root}/") if root else "./"

        for entry in listdir(root):
            full_path = path_join(root, entry)

            if not entry.startswith("."):
                if path_isfile(full_path):
                    files.append(full_path)

                else:
                    files += get_files(full_path)

    except FileNotFoundError:
        print(Text(f"\"{root}\" does not exist").error(), file=stderr, end="\n\n")

    return files

def check(
        rules: dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]],
        paths: list[str],
        silent: int,
        verbose: bool
    ) -> int:

    errors: list[RuleError] | None
    error_count: int = 0
    args : list = paths
    keywords_args: dict
    len_title_line: int

    for category in rules:

        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"entering category \"{category}\" ({rules[category]["name"]})").debug())

        len_title_line = len(f"┏━ {rules[category]["name"]} [•STARTED•] ━┓")
        print("┏━", Text(f"{rules[category]["name"]}").bold(), Text("[•STARTED•]").valid(), "━┓")
        print(Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃"), end="\n")

        for rule in rules[category]:
            if rule in ["name", "info"]:
                continue

            try:
                keywords_args = {}

                for arg in rules[category][rule]["arguments"]:
                    keywords_args[arg] = rules[category][rule]["arguments"][arg]

                keywords_args["verbose"] = verbose

                errors = rules[category][rule]["check"](args, kwargs=keywords_args)

                if errors:
                    error_count += len(errors)

                    if silent != 2:
                        print(Text("┃"), Text(f"{rule}").bold(), Text(f"({len(errors)})").italic(), end="")
                        print(Cursor.move_column(len_title_line - 6) + Text("[KO]").error(), Text(" ┃"), end=("\n" if silent else "\n┃\n"))

                    if not silent:
                        for rule_error in errors:
                            print("┃ " + str(rule_error).replace("\n", str(Color(Color.C_RESET) + "\n┃ ")), end="┃\n", file=stderr)

                elif silent != 2:
                    print(Text("┃"), Text(f"{rule}").bold(), Text("(no error)").italic(), end="")
                    print(Cursor.move_column(len_title_line - 6) + Text("[OK]").valid(), Text(" ┃"), end=("\n" if silent else "\n"))

            except AssertionError:#Exception:
                print(Text("┃"), Text(f"{rule} [FATAL ERROR]").critic(), file=stderr)
                print(Text("┃"), Text(f"terminating JCCS").error(), file=stderr)
                return -1

        print(Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃"), end="\n")
        print("┗━", Text(f"{rules[category]["name"]}").bold(), Text("[••ENDED••]").valid(), "━┛", end="\n\n")

    return error_count

def set_var(
        argv : list[str]
    ) -> None :

    index: int = 0
    while index < len(argv):
        index += 1

def print_help(
    )-> None:
    print(f"""{Text(__program__).bold().underline() + Color(Color.C_RESET)}

C coding style checker for Epitech projects.

Version: {__version__}
Author: {__author__}
Contact: {__email__}

Description:
    JCCS scans a project directory and checks C source files against
    defined coding style rules. Rules are modular and can be executed
    individually or collectively.

Usage:
    JCCS [OPTIONS]

Options:
    {Text("-h").italic() + Color(Color.C_RESET)}, {Text("--help").italic() + Color(Color.C_RESET)}
        Display this help message and exit.

    {Text("-v").italic() + Color(Color.C_RESET)}, {Text("--version").italic() + Color(Color.C_RESET)}
        Show program name, version and author and exit.

    {Text("-r").italic() + Color(Color.C_RESET)}, {Text("--root").italic() + Color(Color.C_RESET)} <path>
        Define the root directory to analyze.
        Default: current directory (.)

    {Text("-R").italic() + Color(Color.C_RESET)}, {Text("--rule").italic() + Color(Color.C_RESET)} <rule_name>
        Run only a specific rule.

    {Text("-R").italic() + Color(Color.C_RESET)}, {Text("--rule").italic() + Color(Color.C_RESET)} "[RULE1 RULE2 ...]"
        Run multiple specific rules (space separated inside brackets).

    {Text("-S").italic() + Color(Color.C_RESET)}, {Text("--set").italic() + Color(Color.C_RESET)} <RULE> <ARG> <VALUE>
        Override a rule argument at runtime.

    {Text("-a").italic() + Color(Color.C_RESET)}, {Text("--show-arguments").italic() + Color(Color.C_RESET)}
        Display all available rules with their descriptions
        and configurable arguments and exit.
    
    {Text("-s").italic() + Color(Color.C_RESET)}, {Text("--silent").italic() + Color(Color.C_RESET)}
        Display only rule summaries (hide detailed error output).

    {Text("--super-silent").italic() + Color(Color.C_RESET)}
        Display only JCCS result (hide detailed error output and summaries).

    {Text("-V").italic() + Color(Color.C_RESET)}, {Text("--verbose").italic() + Color(Color.C_RESET)}
        Enable verbose mode for rules that support it.

Exit codes:
    0       Success (no style errors found)
    84      Failure (style errors detected or invalid usage)
    -1      Fatal internal error during rule execution

Behavior:
    • Recursively scans non-hidden files from the root directory.
    • Applies selected coding style rules.
    • Allows runtime rule filtering and argument configuration.
    • Displays formatted rule results (OK/KO).""")


# Main #
if __name__ == '__main__':

    exit_status : int = EXIT_FAILURE
    error_amount : int = 0
    root : str = "."
    arg_silent : int = 0
    arg_verbose : bool = False

    Console.init(banner=False)

    if len(argv) > 1:

        index: int = 1

        while index < len(argv):

            if argv[index].startswith("-"):
                if argv[index] in ["-V", "--verbose"]:
                    print(Text(" ").debug(title=True), Text(f"Flag: -V/--verbose").debug(), Text("(on)").valid().italic())

                    arg_verbose = True

                elif argv[index] in ["-s", "--silent"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -s/--silent").debug(), Text("(on)").valid().italic())

                    arg_silent = 1

                elif argv[index] in ["--super-silent"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: --super-silent").debug(), Text("(full)").valid().italic())

                    arg_silent = 2

                elif argv[index] in ["-r", "--root"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -r/--root").debug(), Text("(used)").info().italic())

                    if (index + 1) < len(argv):
                        root = argv[index + 1]

                    else:
                        print(Text(f"missing argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                        exit(EXIT_FAILURE)

                elif argv[index] in ["-R", "--rule"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -R/--rule").debug(), Text("(used)").info().italic())

                    new_rules = {}

                    if (index + 1) < len(argv):
                        if argv[index + 1].startswith("[") and argv[index + 1].endswith("]"):
                            new_rules = {
                                "CUSTOM": {
                                    "name": "Custom Rule Selection",
                                    "info": """
Rules selected when calling JCCS
"""
                                }
                            }

                            for arg in argv[index + 1][1:-1].split(" "):
                                rule_exist = False

                                for category in RULES:
                                    if arg in RULES[category]:
                                        new_rules["CUSTOM"][arg] = RULES[category][arg]
                                        rule_exist = True
                                        break

                                if not rule_exist:
                                    print(Text(f"Rule {arg} doesn't exist (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                                    exit(EXIT_FAILURE)

                        else:
                            rule_exist = False

                            for category in RULES:
                                if argv[index + 1] in RULES[category]:
                                    new_rules = {
                                        "CUSTOM": {
                                            "name": "Custom Rule Selection",
                                            "info": """
                                    Rules selected when calling JCCS
                                    """,
                                            argv[index + 1]: RULES[category][argv[index + 1]]
                                        }
                                    }
                                    rule_exist = True
                                    break

                            if not rule_exist:
                                print(Text(f"Rule {argv[index + 1]} doesn't exist (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                                exit(EXIT_FAILURE)

                        RULES = new_rules

                    else:
                        print(Text(f"missing argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                        exit(EXIT_FAILURE)

                elif argv[index] in ["-S", "--set"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -S/--set").debug(), Text("(used)").info().italic())

                    if (index + 3) < len(argv):
                        if argv[index + 1] in RULES:
                            if argv[index + 2] in RULES[argv[index + 1]]["arguments"]:
                                RULES[argv[index + 1]]["arguments"][argv[index + 2]] = argv[index + 3]

                            else:
                                print(Text(f"{argv[index + 1]} doesn't have argument {argv[index + 2]} (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                                exit(EXIT_FAILURE)

                        else:
                            print(Text(f"Rule {argv[index + 1]} doesn't exist (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                            exit(EXIT_FAILURE)

                    else:
                        print(Text(f"missing argument(s) (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                        exit(EXIT_FAILURE)

                elif argv[index] in ["-h", "--help"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -h/--help").debug(), Text("(used)").info().italic())

                    print_help()
                    exit(EXIT_SUCCESS)

                elif argv[index] in ["-v", "--version"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -v/--version").debug(), Text("(used)").info().italic())

                    print(Text(__program__).bold(), Text(__version__).italic(), Text(f"by {__author__}"))
                    exit(EXIT_SUCCESS)

                elif argv[index] in ["-a", "--show-arguments"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -a/--show-arguments").debug(), Text("(used)").info().italic())

                    show_arguments(RULES)
                    exit(EXIT_SUCCESS)

                else:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: invalid").debug(), Text("(error)").error().italic())

                    print(Text(f"invalid argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                    exit(EXIT_FAILURE)

            index += 1

        set_var(argv[1:])

    print(Text("JCCS").bold(), "starting...", start="\n", end="\n\n")

    paths = get_files(root)

    if paths:
        error_amount = check(RULES, paths, silent=arg_silent, verbose=arg_verbose)

    exit_status = (EXIT_FAILURE if error_amount else EXIT_SUCCESS)

    Console.quit(delete_log=True)

    if error_amount > 0:
        print(Text("JCCS").bold(), "finished", Text("[KO]").error(), Text(f"({error_amount} error)").italic())
    elif error_amount == 0:
        print(Text("JCCS").bold(), "finished", Text("[OK]").valid())
    else:
        print(Text("\n") + Text("JCCS").bold().critic() + Text(" terminated").critic(), end="")

    exit(exit_status)
