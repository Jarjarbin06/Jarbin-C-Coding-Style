#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

import jarbin_toolkit_console as Console

from program.rule.rule_manager import RuleManager

print = Console.Console.print
Text = Console.Text.Text
Color = Console.ANSI.Color

Console.init(banner=False)

def get_color(
        text: str,
        level: int,
        title: bool = False,
    ) -> Text:
    lvl_c = {
        0: 96,
        1: 93,
        2: 91,
        3: 95
    }
    t: int = 10 if title else 0
    if level in lvl_c:
        return Text(Color(lvl_c[level] + t) + text)
    return Text(Color(97 + t) + text)

def get_level(
        level: int
    ) -> str:
    lvl_s = {
        0: "INFO",
        1: "MINOR",
        2: "MAJOR",
        3: "FATAL"
    }

    if level in lvl_s:
        return lvl_s[level]
    return f"UNKNOWN ({level})"

def show_arguments(manager: RuleManager) -> None:
    """
    Displays:
    Category → Rule → Info → Arguments
    """

    categories = list(manager.categories.values())

    print("=" * 60)
    print(Text("   JCCS - RULES   ").bold())
    print("=" * 60)

    last_category = categories[-1] if categories else None

    for category in categories:

        print(f"{Text(category.language).bold()}", end="")
        print(f" ─ {Text(category.name).bold()}", end="")
        print(f" ─ {Text(category.title).italic()}")
        print(Text(category.info).dim())
        print("─" * 60)

        rules = list(category.rules.values())
        last_rule = rules[-1] if rules else None

        for rule in rules:

            # RULE HEADER

            print(f"{Text(rule.language).italic().bold()}", end="")
            print(f" ─ {Text(rule.name).underline().bold()}")
            print(Text(rule.info).dim())

            print(Text(f"Level: {get_color(get_level(rule.level), rule.level)}").italic())

            # ARGUMENTS
            print(Text("Arguments:").bold())

            if not rule.variables:
                print(Text("  (no argument)").italic().dim())
            else:
                for arg_name, arg_value in rule.variables.items():

                    # expected format: VAR_NAME = value or tuple/list
                    value = arg_value

                    desc = None
                    if isinstance(arg_value, (tuple, list)) and len(arg_value) >= 2:
                        value = arg_value[0]
                        desc = arg_value[1]

                    print(
                        f"  - {arg_name.removeprefix('VAR_')} : \"{value}\"",
                        end=""
                    )

                    if desc:
                        print(f"\n    {Text(f'[ {desc} ]').italic().dim()}")
                    else:
                        print(f"\n    {Text('[ No description ]').italic().dim()}")

            if rule is not last_rule:
                print("─" * 60)

        if category is not last_category:
            print("\n" + "═" * 60)


    print("═" * 60)

def print_help(
        simplename: str,
        fullname: str,
        version: str,
        author: str,
        email: str
    )-> None:
    app_c: dict[str, str] = {
        "NAME": Color.rgb_fg(0, 255, 200).s,
        "HEADER": Color.rgb_fg(0, 180, 255).s,
        "FLAG": Color.rgb_fg(255, 215, 0).s,
        "ARGUMENT": Color.rgb_fg(255, 170, 60).s,
        "SUCCESS": Color.rgb_fg(80, 220, 120).s,
        "ERROR": Color.rgb_fg(255, 80, 80).s,
        "CRITIC": Color.rgb_fg(255, 80, 80).s + Color.rgb_bg(0, 0, 0).s,
        "ADVANCED": Color.rgb_fg(180, 120, 255).s,
        "WARNING": Color.rgb_fg(255, 140, 60).s,
        "DIM": Color.rgb_fg(120, 120, 120).s,
        "RESET": Color(Color.C_RESET).s
    }
    print(f"""
{app_c["NAME"] + Text(f"{simplename} ({fullname})").bold().s + app_c["RESET"]}
C Coding Style Checker for Epitech Projects

Version : {Text(version).italic() + app_c["RESET"]}
Author  : {Text(author).italic() + app_c["RESET"]}
Contact : {Text(email).italic() + app_c["RESET"]}

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}DESCRIPTION{app_c["RESET"]}
    {app_c["NAME"] + simplename + app_c["RESET"]} recursively scans a project directory and analyzes C source
    files according to modular coding style rules.

    Rules can be:
        • Executed collectively (default behavior)
        • Filtered individually
        • Configured dynamically at runtime

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}USAGE{app_c["RESET"]}
    {app_c["NAME"] + simplename + app_c["RESET"]} [{app_c["FLAG"] + "-h" + app_c["RESET"]}] [{app_c["FLAG"] + "--help" + app_c["RESET"]}] [{app_c["FLAG"] + "-v" + app_c["RESET"]} | {app_c["FLAG"] + "--version" + app_c["RESET"]}] [{app_c["FLAG"] + "-a" + app_c["RESET"]} | {app_c["FLAG"] + "--show-arguments" + app_c["RESET"]}] [{app_c["FLAG"] + "--update" + app_c["RESET"]}]
    {" " * len(simplename)} [{app_c["FLAG"] + "-r" + app_c["RESET"]} {app_c["ARGUMENT"] + "<path>" + app_c["RESET"]}] [{app_c["FLAG"] + "-e" + app_c["RESET"]} {app_c["ARGUMENT"] + "<path> ..." + app_c["RESET"]}]
    {" " * len(simplename)} [{app_c["FLAG"] + "-R" + app_c["RESET"]} {app_c["ARGUMENT"] + "<rule> ..." + app_c["RESET"]}] [{app_c["FLAG"] + "-S" + app_c["RESET"]} {app_c["ARGUMENT"] + "<CATEGORY> <RULE> <ARG> <VALUE>" + app_c["RESET"]}]
    {" " * len(simplename)} [{app_c["FLAG"] + "-s" + app_c["RESET"]} | {app_c["FLAG"] + "--silent" + app_c["RESET"]} | {app_c["FLAG"] + "--super-silent" + app_c["RESET"]} | {app_c["FLAG"] + "--extreme-silent" + app_c["RESET"]}]
    {" " * len(simplename)} [{app_c["FLAG"] + "-V" + app_c["RESET"]} | {app_c["FLAG"] + "--verbose" + app_c["RESET"]} | {app_c["FLAG"] + "--super-verbose" + app_c["RESET"]}]
    {" " * len(simplename)} [{app_c["FLAG"] + "-j" + app_c["RESET"]} | {app_c["FLAG"] + "--json-log" + app_c["RESET"]}] [{app_c["FLAG"] + "--no-log" + app_c["RESET"]}] [{app_c["FLAG"] + "--show-log" + app_c["RESET"]}]

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}GENERAL OPTIONS{app_c["RESET"]}

    {app_c["FLAG"] + Text("-h").italic().s + app_c["RESET"]}
            Display the simple help message and exit.

        {app_c["FLAG"] + Text("--help").italic().s + app_c["RESET"]}
            Display this help message and exit.

    {app_c["FLAG"] + Text("-v").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--version").italic().s + app_c["RESET"]}
            Display program name, version and author, then exit.

    {app_c["FLAG"] + Text("-a").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--show-arguments").italic().s + app_c["RESET"]}
            Display all available rule categories, rules,
            and their configurable arguments, then exit.

        {app_c["FLAG"] + Text("--update").italic().s + app_c["RESET"]}
            Update {app_c["NAME"] + simplename + app_c["RESET"]} using the internal update script and exit.

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}PROJECT CONFIGURATION{app_c["RESET"]}

    {app_c["FLAG"] + Text("-r").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--root").italic().s + app_c["RESET"]} {app_c["ARGUMENT"] + "<path>" + app_c["RESET"]}
            Define the root directory to analyze.
            Default: current directory (.)

    {app_c["FLAG"] + Text("-e").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--exclude").italic().s + app_c["RESET"]} {app_c["ARGUMENT"] + "<path1> [path2 ...]" + app_c["RESET"]}
            Exclude one or multiple paths from scanning.
            • Accepts space-separated values.
            • Can be used multiple times.
            • Values may also be passed inside quotes.

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}RULE SELECTION & CONFIGURATION{app_c["RESET"]}

    {app_c["FLAG"] + Text("-R").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--rule").italic().s + app_c["RESET"]} {app_c["ARGUMENT"] + "<rule1> [rule2 ...]" + app_c["RESET"]}
            Execute only the specified rule(s).
            • Accepts multiple rule names.
            • Replaces default rule set with a custom selection.
            • Fails if a rule does not exist.
            {app_c["ADVANCED"] + Text("use carefully").italic().bold().s + app_c["RESET"]}

    {app_c["FLAG"] + Text("-S").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--set").italic().s + app_c["RESET"]} {app_c["ARGUMENT"] + "<CATEGORY> <RULE> <ARG> <VALUE>" + app_c["RESET"]}
            Override a rule argument at runtime.
            • CATEGORY must exist.
            • RULE must exist in the category.
            • ARG must be configurable.
            • VALUE replaces the default argument value.
            {app_c["ADVANCED"] + Text("use carefully").italic().bold().s + app_c["RESET"]}

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}OUTPUT CONTROL{app_c["RESET"]}

    {app_c["FLAG"] + Text("-s").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--silent").italic().s + app_c["RESET"]}
            Silent mode (level 1):
            Display rule summaries only.

        {app_c["FLAG"] + Text("--super-silent").italic().s + app_c["RESET"]}
            Silent mode (level 2):
            Display only the final {app_c["NAME"] + simplename + app_c["RESET"]} result.

        {app_c["FLAG"] + Text("--extreme-silent").italic().s + app_c["RESET"]}
            Silent mode (level 3):
            No output at all.

    {app_c["FLAG"] + Text("-V").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--verbose").italic().s + app_c["RESET"]}
            Verbose mode (level 1):
            Display category and rule execution debug output.

        {app_c["FLAG"] + Text("--super-verbose").italic().s + app_c["RESET"]}
            Verbose mode (level 2):
            Display full execution trace including rule timings.
            {app_c["WARNING"] + Text("may increase output").italic().bold().s + app_c["RESET"]}

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}LOGGING{app_c["RESET"]}

    {app_c["FLAG"] + Text("-j").italic().s + app_c["RESET"]}, {app_c["FLAG"] + Text("--json-log").italic().s + app_c["RESET"]}
            Switch log format to JSON.
            Default format: JAR-LOG.

        {app_c["FLAG"] + Text("--no-log").italic().s + app_c["RESET"]}
            Disable log file creation at runtime end.

        {app_c["FLAG"] + Text("--show-log").italic().s + app_c["RESET"]}
            Print generated log at program termination.
            {app_c["WARNING"] + Text("may increase output").italic().bold().s + app_c["RESET"]}

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}EXIT CODES{app_c["RESET"]}

    {app_c["SUCCESS"] + "0" + app_c["RESET"]}       Success — No style errors detected
    {app_c["ERROR"] + "84" + app_c["RESET"]}      Failure — Style errors detected or invalid usage
    {app_c["CRITIC"] + "1" + app_c["RESET"]}       Fatal internal error during {app_c["NAME"] + simplename + app_c["RESET"]} execution

{app_c["DIM"]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{app_c["RESET"]}

{app_c["HEADER"]}BEHAVIOR{app_c["RESET"]}

    • Recursively scans non-hidden files from the root directory.
    • Ignores hidden files and directories (starting with ".").
    • Applies selected coding style rules sequentially by category.
    • Supports runtime rule filtering ({app_c["FLAG"] + "-R" + app_c["RESET"]}).
    • Supports runtime argument overrides ({app_c["FLAG"] + "-S" + app_c["RESET"]}).
    • Produces structured rule results ({app_c["SUCCESS"] + "OK" + app_c["RESET"]} / {app_c["ERROR"] + "KO" + app_c["RESET"]}).
    • Logs execution unless disabled.
    • Supports multiple silent levels (1 → summary, 3 → no output).
""")

def print_usage(
        simplename: str
    )-> None:
    print(
f"""usage: {simplename} [-h] [--help] [-v | --version] [-a | --show-arguments] [--update]
       {" " * len(simplename)} [-r <path>] [-e <path> ...]
       {" " * len(simplename)} [-R <rule> ...] [-S <CATEGORY> <RULE> <ARG> <VALUE>]
       {" " * len(simplename)} [-s | --silent | --super-silent | --extreme-silent]
       {" " * len(simplename)} [-V | --verbose | --super-verbose]
       {" " * len(simplename)} [-j | --json-log] [--no-log] [--show-log]

C Coding Style Checker for Epitech Projects

General options:
   -h                      Show this help message and exit
       --help              Show the full help message and exit
   -v, --version           Show program version and author
   -a, --show-arguments    List all rules and configurable arguments
       --update            Update the program and exit

Project configuration:
   -r, --root <path>       Set root directory (default: .)
   -e, --exclude <path>    Exclude paths (can be repeated)

Rule selection:
   -R, --rule <rule>       Run only specified rule(s)
   -S, --set <C R A V>     Override rule argument (CATEGORY RULE ARG VALUE)

Output control:
   -s, --silent            Minimal output
       --super-silent      Only final result
       --extreme-silent    No output
   -V, --verbose           Debug output
       --super-verbose     Full execution trace

Logging:
   -j, --json-log          Use JSON log format
       --no-log            Disable log file
       --show-log          Print log at the end

Exit codes:
   0   Success
   84  Failure (style error or invalid usage)
   1   Fatal internal error

Run '{simplename} --help' for full documentation."""
    )
