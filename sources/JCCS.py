#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


# Program imports #
from os import walk
from os.path import join as path_join, abspath, normpath
from sys import argv, stderr, exit
from typing import Callable, Any
from Error import RuleError
import jarbin_toolkit_console as Console
from jarbin_toolkit_log import Log
import jarbin_toolkit_time as Time
from subprocess import Popen, DEVNULL

print = Console.Console.print
Text = Console.Text.Text
Color = Console.ANSI.Color
Cursor = Console.ANSI.Cursor
Animation = Console.Animation

Console.init(banner=False)

EXIT_SUCCESS = 0
EXIT_FAILURE = 84
EXIT_FATAL = 1
RULES: dict[str, str | dict[str, str | dict[str, str | Callable | dict[str, Any]]]]


# Program info #
__program__ = "JCCS (Jarbin-C-Coding-Style)"
__version__ : str = open(abspath(__file__).removesuffix("sources/JCCS.py") + "VERSION", 'r').read()
__author__ : str = "Jarjarbin06"
__email__ : str = "nathan.amaraggi@epitech.eu"


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

def update_jccs() -> None:
    spinner = Animation.Spinner.stick(style=Animation.Style(border_left="[", border_right="]")).warning()
    update_script = f"{abspath(__file__).removesuffix("sources/JCCS.py")}scripts/update-jccs"
    proc = Popen(["bash", str(update_script)], stdout=DEVNULL, stderr=DEVNULL)

    while proc.poll() is None:
        spinner()
        print(Text("JCCS").bold(), ":", Text(f"updating {spinner.render()}").warning() + Cursor.previous(), sleep=0.1)

    print(Text("JCCS").bold(), ":", Text("successfully updated").valid())

def get_files(
        root: str = "./",
        excludes: list[str] | None = None,
    ) -> list[str]:

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

def check(
        rules: dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]],
        paths: list[str],
        silent: int = 0,
        verbose: int = 0
    ) -> int:

    errors: list[RuleError] | None = None
    category_error_count: int = 0
    error_count: int = 0
    args : list = paths
    keywords_args: dict
    len_title_line: int
    show_category_boxes = silent != 2
    show_rule_errors = silent == 0
    jccs_timer = Time.StopWatch()
    category_timer = Time.StopWatch()
    rule_timer = Time.StopWatch()
    log.log("INFO", "Rule", f"*args set")

    if log_type == "jar-log":
        log.comment(f"*args set to paths")

    jccs_timer.start()

    for category in rules:

        category_timer.start()
        category_error_count = 0

        if verbose:
            print(Text(" ").debug(title=True), Text(f"entering category \"{category}\" ({rules[category]["name"]})").debug())

        log.log("INFO", "Category", f"entering category {repr(category)}")
        len_title_line = len(f"┏━ {rules[category]["name"]} [•STARTED•] ━┓")

        if show_category_boxes:
            print("┏━", Text(f"{rules[category]["name"]}").bold(), Text("[•STARTED•]").valid(), "━┓")
            print(Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃"), end="\n")

        for rule in rules[category]:
            if rule in ["name", "info"]:
                continue

            try:

                log.log("INFO", f"Rule {rule}", f"entering rule {repr(rule)}")
                if log_type == "jar-log":
                    log.comment(f"{rule} rule info:{rules[category][rule]["info"]}")
                keywords_args = {}

                for arg in rules[category][rule]["arguments"]:
                    keywords_args[arg] = rules[category][rule]["arguments"][arg]

                keywords_args["verbose"] = verbose

                log.log("INFO", f"Rule {rule}", f"**kwargs set")
                if log_type == "jar-log":
                    log.comment(f"**kwargs = {repr(keywords_args)}")

                rule_timer.start()
                log.log("INFO", f"Rule {rule}", f"launching {repr(rule)} rule check")
                errors = rules[category][rule]["check"](args, kwargs=keywords_args)
                log.log("INFO", f"Rule {rule}", f"ending {repr(rule)} rule check")
                rule_time = round(rule_timer.elapsed(), 10)

                if verbose:
                    print(Text(" ").debug(title=True), Text(f"elapsed time for {category}/{rule} : {rule_time}").debug())

                if log_type == "jar-log":
                    log.comment(f"elapsed time for {category}/{rule} : {rule_time}")

                rule_timer.reset()

                if errors:

                    log.log("INFO", f"Rule {rule}", f"errors found ({len(errors)} errors)")
                    category_error_count += len(errors)

                    if show_category_boxes:
                        print(Text("┃").error(), Text(f"{rule}").bold().error(), Text(f"({len(errors)})").italic().error(), end="")
                        print(Cursor.move_column(len_title_line - 6) + Text("[KO]").error(), Text(" ┃").error(), Text("◀").error(), end=("\n┃\n" if show_rule_errors else "\n"))

                    for rule_error in errors:
                        log.log("ERROR", f"Rule {rule}", f"{rule_error.message.split("\n")[0]}")

                        if show_rule_errors:
                            print("┃ " + str(rule_error).replace("\n", str(Color(Color.C_RESET) + "\n┃ ")), end="┃\n", file=stderr)

                elif show_category_boxes:
                    print(Text("┃"), Text(f"{rule}").bold(), Text("(no error)").italic(), end="")
                    print(Cursor.move_column(len_title_line - 6) + Text("[OK]").valid(), Text(" ┃"), end=("\n" if show_rule_errors else "\n"))

                log.log("INFO", f"Rule {rule}", f"leaving rule {repr(rule)}")

            except Exception as err:

                log.log("CRIT", f"Rule {rule}", f"{str(err)}")

                if show_category_boxes:
                    print(Text("┃"), Text(f"{rule} [FATAL ERROR]").critic(), file=stderr)
                    print(Text("┃"), Text(f"terminating JCCS").error(), file=stderr)
                    print("┗━", Text(f"{rules[category]["name"]} ").bold(), (Text("[••TERM••]").critic() if category_error_count else Text("[••ENDED••]").valid()), "━┛", end="\n\n")
                return -1

        if show_category_boxes:
            print(Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃"), end="\n")
            print("┗━", Text(f"{rules[category]["name"]}").bold(), (Text("[••ENDED••]").error() if category_error_count else Text("[••ENDED••]").valid()), "━┛", end="\n\n")

        error_count += category_error_count
        category_time = round(category_timer.elapsed(), 10)

        if verbose:
            print(Text(" ").debug(title=True), Text(f"elapsed time for {category} : {category_time}").debug())
            print(Text(" ").debug(title=True), Text(f"leaving category \"{category}\" ({rules[category]["name"]})").debug(), Text(f"({category_error_count} errors found)").error() if category_error_count else Text("(no error)").valid())

        if log_type == "jar-log":
            log.comment(f"elapsed time for {category} : {category_time}")

        category_timer.reset()

    jccs_time = round(jccs_timer.elapsed(), 10)

    if verbose:
        print(Text(" ").debug(title=True), Text(f"total elapsed time : {jccs_time}").debug())

    if log_type == "jar-log":
        log.comment(f"total elapsed time : {jccs_time}")

    return error_count

def print_help(
    )-> None:
    print(f"""
{Text(__program__).bold() + Color(Color.C_RESET)}

C Coding Style Checker for Epitech Projects

Version : {__version__}
Author  : {__author__}
Contact : {__email__}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESCRIPTION
    JCCS recursively scans a project directory and analyzes C source
    files according to modular coding style rules.

    Rules can be:
        • Executed collectively (default behavior)
        • Filtered individually
        • Configured dynamically at runtime

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USAGE
    JCCS [OPTIONS]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GENERAL OPTIONS

    {Text("-h").italic() + Color(Color.C_RESET)}, {Text("--help").italic() + Color(Color.C_RESET)}
        Display this help message and exit.

    {Text("-v").italic() + Color(Color.C_RESET)}, {Text("--version").italic() + Color(Color.C_RESET)}
        Display program name, version and author, then exit.

    {Text("-a").italic() + Color(Color.C_RESET)}, {Text("--show-arguments").italic() + Color(Color.C_RESET)}
        Display all available rule categories, rules,
        and their configurable arguments, then exit.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT CONFIGURATION

    {Text("-r").italic() + Color(Color.C_RESET)}, {Text("--root").italic() + Color(Color.C_RESET)} <path>
        Define the root directory to analyze.
        Default: current directory (.)

    {Text("-e").italic() + Color(Color.C_RESET)}, {Text("--exclude").italic() + Color(Color.C_RESET)} <path1> [path2 ...]
        Exclude one or multiple paths from scanning.
        • Accepts space-separated values.
        • Can be used multiple times.
        • Values may also be passed inside quotes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE SELECTION & CONFIGURATION

    {Text("-R").italic() + Color(Color.C_RESET)}, {Text("--rule").italic() + Color(Color.C_RESET)} <rule1> [rule2 ...]
        Execute only the specified rule(s).
        • Accepts multiple rule names.
        • Replaces default rule set with a custom selection.
        • Fails if a rule does not exist.

    {Text("-S").italic() + Color(Color.C_RESET)}, {Text("--set").italic() + Color(Color.C_RESET)} <CATEGORY> <RULE> <ARG> <VALUE>
        Override a rule argument at runtime.
        • CATEGORY must exist.
        • RULE must exist in the category.
        • ARG must be configurable.
        • VALUE replaces the default argument value.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OUTPUT CONTROL

    {Text("-s").italic() + Color(Color.C_RESET)}, {Text("--silent").italic() + Color(Color.C_RESET)}
        Silent mode (level 1):
        Display rule summaries only.

    {Text("--super-silent").italic() + Color(Color.C_RESET)}
        Silent mode (level 2):
        Display only the final JCCS result.

    {Text("-V").italic() + Color(Color.C_RESET)}, {Text("--verbose").italic() + Color(Color.C_RESET)}
        Verbose mode (level 1):
        Enable additional rule-level debugging output.

    {Text("--super-verbose").italic() + Color(Color.C_RESET)}
        Verbose mode (level 2):
        Enable full detailed rule execution output.
        (May significantly increase terminal output.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOGGING

    {Text("-j").italic() + Color(Color.C_RESET)}, {Text("--json-log").italic() + Color(Color.C_RESET)}
        Switch log format to JSON.
        Default format: JAR-LOG.

    {Text("--no-log").italic() + Color(Color.C_RESET)}
        Delete the log file at program termination.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXIT CODES

    0       Success — No style errors detected
    84      Failure — Style errors detected or invalid usage
    1       Fatal internal error during rule execution

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEHAVIOR

    • Recursively scans non-hidden files from the root directory.
    • Applies selected coding style rules.
    • Supports runtime rule filtering and argument overrides.
    • Produces structured rule results (OK / KO).
    • Logs execution details unless disabled.
""")


# Main #
if __name__ == '__main__':

    exit_status : int = EXIT_FAILURE
    error_amount : int = 0
    root : str = "."
    arg_silent : int = 0
    arg_verbose : int = 0
    arg_exclude : list = []
    log_type : str = "jar-log"
    arg_no_log : bool = False

    if Log.exist("."):
        log = Log(".", "JCCS")
        log.delete()

    log = Log(".", "JCCS")

    try:
        from rules import Rules

    except Exception:
        print(Text("Failed to import the rules").critic())
        exit(EXIT_FATAL)

    else:
        RULES = Rules.RULES

    if "-j" in argv or "--json-log" in argv:
        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"Flag: -j/--json-log").debug(), Text("(on)").info().italic())

        log_type = "json"
        log.delete()
        log = Log(".", "JCCS", True)

    if "--no-log" in argv:
        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"Flag: --no-log").debug(), Text("(on)").info().italic())
        arg_no_log = True

    if "-V" in argv or "--verbose" in argv:
        print(Text(" ").debug(title=True), Text(f"Flag: -V/--verbose").debug(), Text("(on)").valid().italic())

        log.log("VALID", "Flag", "-V/--verbose activated")
        arg_verbose = 1

    if "--super-verbose" in argv:
        print(Text(" ").debug(title=True), Text(f"Flag: --super-verbose").debug(), Text("(full)").valid().italic())

        log.log("VALID", "Flag", "--super-verbose activated")
        arg_verbose = 2

    if "-s" in argv or "--silent" in argv:
        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"Flag: -s/--silent").debug(), Text("(on)").valid().italic())

        log.log("VALID", "Flag", "-s/--silent activated")
        arg_silent = 1

    if "--super-silent" in argv:
        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"Flag: --super-silent").debug(), Text("(full)").valid().italic())

        log.log("VALID", "Flag", "--super-silent activated")
        arg_silent = 2

    if len(argv) > 1:

        index: int = 1

        while index < len(argv):

            if argv[index].startswith("-"):
                if argv[index] in ["-j", "--json-log"]:
                    index += 1

                elif argv[index] in ["--no-log"]:
                    index += 1

                elif argv[index] in ["-V", "--verbose"]:
                    index += 1

                elif argv[index] in ["--super-verbose"]:
                    index += 1

                elif argv[index] in ["-s", "--silent"]:
                    index += 1

                elif argv[index] in ["--super-silent"]:
                    index += 1

                elif argv[index] in ["-r", "--root"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -r/--root").debug(), Text("(used)").info().italic())

                    if (index + 1) < len(argv):
                        root = argv[index + 1]
                        index += 2
                        log.log("VALID", "Flag", f"-r/--root set to {repr(root)}")

                    else:
                        print(Text(f"missing argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                        log.log("ERROR", "Flag", f"-r/--root failed to set to new value")
                        log.close()
                        if arg_no_log:
                            log.delete()
                        exit(EXIT_FAILURE)

                elif argv[index] in ["-e", "--exclude"]:
                    if arg_verbose:
                        print( Text(" ").debug(title=True), Text("Flag: -e/--exclude").debug(), Text("(used)").info().italic())

                    if (index + 1) < len(argv):
                        collected_excludes = []
                        i = index + 1

                        while i < len(argv) and not argv[i].startswith("-"):
                            if " " in argv[i]:
                                collected_excludes.extend(argv[i].split(" "))
                            else:
                                collected_excludes.append(argv[i])
                            i += 1

                        if not collected_excludes:
                            print(Text(f"missing argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                            log.log("ERROR", "Flag", "-e/--exclude failed to set to new value")
                            log.close()
                            if arg_no_log:
                                log.delete()
                            exit(EXIT_FAILURE)

                        if not isinstance(arg_exclude, list):
                            arg_exclude = []

                        for path in collected_excludes:
                            if path not in arg_exclude:
                                arg_exclude.append(path)

                        log.log("VALID", "Flag", f"-e/--exclude set to {repr(arg_exclude)}")
                        index = i

                    else:
                        print(Text(f"missing argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                        log.log("ERROR", "Flag", "-e/--exclude failed to set to new value")
                        log.close()
                        if arg_no_log:
                            log.delete()
                        exit(EXIT_FAILURE)

                elif argv[index] in ["-R", "--rule"]:

                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -R/--rule").debug(), Text("(used)").info().italic())

                    new_rules = {}

                    if (index + 1) < len(argv):
                        collected_rules = []
                        i = index + 1

                        while i < len(argv) and not argv[i].startswith("-"):
                            if " " in argv[i]:
                                collected_rules.extend(argv[i].split(" "))

                            else:
                                collected_rules.append(argv[i])

                            i += 1

                        if not collected_rules:
                            print(Text(f"missing argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                            log.log("ERROR", "Flag", f"-R/--rule failed to set to new value")
                            log.close()
                            if arg_no_log:
                                log.delete()
                            exit(EXIT_FAILURE)

                        new_rules = {
                            "CUSTOM": {
                                "name": "Custom Rule Selection",
                                "info": """
                Rules selected when calling JCCS
                """
                            }
                        }

                        for arg in collected_rules:
                            rule_exist = False

                            for category in RULES:
                                if arg in RULES[category]:
                                    new_rules["CUSTOM"][arg] = RULES[category][arg]
                                    rule_exist = True
                                    break

                            if not rule_exist:
                                print(Text(f"Rule {arg} doesn't exist (\"{argv[index]}\" near position {index + 1})").error(), file=stderr)
                                log.log("ERROR", "Flag", f"-R/--rule failed to set to new value")
                                log.close()
                                if arg_no_log:
                                    log.delete()
                                exit(EXIT_FAILURE)

                        RULES = new_rules
                        log.log("VALID", "Flag", f"-R/--rule new rules set")
                        index = i

                    else:
                        print(Text(f"missing argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                        log.log("ERROR", "Flag", f"-R/--rule failed to set to new value")
                        log.close()
                        if arg_no_log:
                            log.delete()
                        exit(EXIT_FAILURE)

                elif argv[index] in ["-S", "--set"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -S/--set").debug(), Text("(used)").info().italic())

                    if (index + 4) < len(argv):
                        if argv[index + 1] in RULES:
                            if argv[index + 2] in RULES[argv[index + 1]]:
                                if argv[index + 3] in RULES[argv[index + 1]][argv[index + 2]]["arguments"]:
                                    log.log("VALID", "Flag", f"-S/--set {repr(argv[index + 1])}/{repr(argv[index + 2])}/{repr(argv[index + 3])} set to {repr(argv[index + 4])}")
                                    RULES[argv[index + 1]][argv[index + 2]]["arguments"][argv[index + 3]] = argv[index + 4]
                                    index += 5

                                else:
                                    print(Text(f"{argv[index + 2]} in {argv[index + 1]} doesn't have argument {argv[index + 3]} (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                                    log.log("ERROR", "Flag", f"-S/--set failed to set to new value")
                                    log.close()
                                    if arg_no_log:
                                        log.delete()
                                    exit(EXIT_FAILURE)

                            else:
                                print(Text(f"Rule {argv[index + 2]} doesn't exist in {argv[index + 1]} (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                                log.log("ERROR", "Flag", f"-S/--set failed to set to new value")
                                log.close()
                                if arg_no_log:
                                    log.delete()
                                exit(EXIT_FAILURE)

                        else:
                            print(Text(f"Category {argv[index + 1]} doesn't exist (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                            log.log("ERROR", "Flag", f"-S/--set failed to set to new value")
                            log.close()
                            if arg_no_log:
                                log.delete()
                            exit(EXIT_FAILURE)

                    else:
                        print(Text(f"missing argument(s) (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                        log.log("ERROR", "Flag", f"-S/--set failed to set to new value")
                        log.close()
                        if arg_no_log:
                            log.delete()
                        exit(EXIT_FAILURE)

                elif argv[index] in ["-h", "--help"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -h/--help").debug(), Text("(used)").info().italic())

                    log.log("VALID", "Flag", f"-h/--help used")
                    print_help()
                    log.close()
                    if arg_no_log:
                        log.delete()
                    exit(EXIT_SUCCESS)

                elif argv[index] in ["-v", "--version"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -v/--version").debug(), Text("(used)").info().italic())

                    log.log("VALID", "Flag", f"-v/--version used")
                    print(Text(__program__).bold(), Text(__version__).italic(), Text(f"by {__author__}"))
                    log.close()
                    if arg_no_log:
                        log.delete()
                    exit(EXIT_SUCCESS)

                elif argv[index] in ["-a", "--show-arguments"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: -a/--show-arguments").debug(), Text("(used)").info().italic())

                    log.log("VALID", "Flag", f"-a/--show-argument used")
                    show_arguments(RULES)
                    log.close()
                    if arg_no_log:
                        log.delete()
                    exit(EXIT_SUCCESS)

                elif argv[index] in ["--update"]:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: --update").debug(), Text("(used)").info().italic())

                    log.log("VALID", "Flag", f"--update used")
                    update_jccs()
                    log.close()
                    if arg_no_log:
                        log.delete()
                    exit(EXIT_SUCCESS)

                else:
                    if arg_verbose:
                        print(Text(" ").debug(title=True), Text(f"Flag: invalid").debug(), Text("(error)").error().italic())

                    print(Text(f"invalid argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                    log.log("ERROR", "Flag", f"invalid flag {repr({argv[index]})}")
                    log.close()
                    if arg_no_log:
                        log.delete()
                    exit(EXIT_FAILURE)

            else:
                print(Text(f"invalid argument (\"{argv[index]}\" at position {index + 1})").error(), file=stderr)
                log.log("ERROR", "Arg", f"invalid argument {repr({argv[index]})}")
                log.close()
                if arg_no_log:
                    log.delete()
                exit(EXIT_FAILURE)

    if arg_verbose:
        print(Text(" ").debug(title=True), Text(f"starting JCCS").debug())

    print(Text("JCCS").bold(), "starting...", start="\n", end="\n\n")
    paths = get_files(root, arg_exclude)
    log.log("INFO", "Program", f"{len(paths)} paths found")

    if arg_verbose:
        print(Text(" ").debug(title=True), Text(f"{len(paths)} paths found").debug())

    if paths:
        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"starting check").debug())

        log.log("INFO", "Program", f"start check")
        error_amount = check(RULES, paths, silent=arg_silent, verbose=arg_verbose)
        log.log("INFO", "Program", "check finished" + (f" with {error_amount} errors" if error_amount > 0 else " (fatal error)"))

        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"ending check").debug())

    exit_status = (EXIT_FAILURE if error_amount > 0 else EXIT_SUCCESS)

    if error_amount > 0:
        print(Text("JCCS").bold(), "finished", Text("[KO]").error(), Text(f"({error_amount} error)").italic())
        log.log("ERROR", "Program", f"JCCS terminated with {error_amount} error")
    elif error_amount == 0:
        print(Text("JCCS").bold(), "finished", Text("[OK]").valid())
        log.log("VALID", "Program", f"JCCS terminated with success")
    else:
        print(Text("JCCS").bold().critic() + Text(" terminated").critic())
        log.log("CRIT", "Program", f"JCCS terminated due to an internal error")
        exit_status = EXIT_FATAL

    if arg_verbose:
        print(Text(" ").debug(title=True), Text(f"ending JCCS").debug())

    log.close()
    if arg_no_log:
        log.delete()

    exit(exit_status)

Console.quit(delete_log=True)
