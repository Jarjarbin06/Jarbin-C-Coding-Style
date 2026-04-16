#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from sys import stderr
from typing import Callable

from jarbin_toolkit_console.Text import Text
from jarbin_toolkit_log import Log

import program.helper as Helper
from program.update import update_jccs

EXIT_SUCCESS = 0
EXIT_FAILURE = 84

class Flag:

    def __init__(
        self,
        names: list[str],
        has_value: bool = False,
        multi: bool = False,
        handler: str | Callable | None = None,
        description: str = ""
    ) -> None:
        self.names: list[str] = names
        self.has_value: bool = has_value
        self.multi: bool = multi
        self.handler: str | Callable | None = handler
        self.description: str = description

    def __call__(
            self,
            *args,
            **kwargs
        ) -> None:
        self.handler(*args, **kwargs)

class Context:

    def __init__(
            self,
            log
        ) -> None:
        self.root: str = "."
        self.silent: int = 0
        self.verbose: int = 0
        self.exclude: list[str] = []
        self.no_log: bool = False
        self.show_log: bool = False
        self.log: Log = log
        self.rules = None

def error(
        msg,
        ctx: Context
    ) -> None:
    print(Text(msg).error(), file=stderr)
    ctx.log.log("ERROR", "Flag", msg)
    ctx.log.close()
    exit(EXIT_FAILURE)

def parse_args(
        argv,
        ctx: Context,
        simplename: str,
        fullname: str,
        version: str,
        author: str,
        email: str
    ) -> Context:
    i = 1

    # =========================
    # HANDLERS
    # =========================

    def handle_json(
            values
        ) -> None:
        ctx.log_type = "json"
        ctx.log.delete()
        ctx.log = Log(".", "JCCS", True)
        ctx.log.log("VALID", "Flag", "-j/--json-log activated")

    def handle_verbose(
            values
        ) -> None:
        print(Text(" ").debug(title=True), Text("Flag: -V/--verbose").debug(), Text("(on)").valid().italic())
        ctx.log.log("VALID", "Flag", "-V/--verbose activated")
        ctx.verbose = 1

    def handle_super_verbose(
            values
        ) -> None:
        print(Text(" ").debug(title=True), Text("Flag: --super-verbose").debug(), Text("(full)").valid().italic())
        ctx.log.log("VALID", "Flag", "--super-verbose activated")
        ctx.verbose = 2

    def handle_no_log(
            values
        ) -> None:
        if ctx.verbose:
            print(Text(" ").debug(title=True), Text("Flag: --no-log").debug(), Text("(on)").info().italic())
        ctx.log.log("VALID", "Flag", "--no-log activated")
        ctx.no_log = True

    def handle_show_log(
            values
        ) -> None:
        if ctx.verbose:
            print(Text(" ").debug(title=True), Text("Flag: --show-log").debug(), Text("(on)").info().italic())
        ctx.log.log("VALID", "Flag", "--show-log activated")
        ctx.show_log = True

    def handle_silent(
            values
        ) -> None:
        if ctx.verbose:
            print(Text(" ").debug(title=True), Text("Flag: -s/--silent").debug(), Text("(on)").valid().italic())
        ctx.log.log("VALID", "Flag", "-s/--silent activated")
        ctx.silent = 1

    def handle_super_silent(
            values
        ) -> None:
        if ctx.verbose:
            print(Text(" ").debug(title=True), Text("Flag: --super-silent").debug(), Text("(full)").valid().italic())
        ctx.log.log("VALID", "Flag", "--super-silent activated")
        ctx.silent = 2

    def handle_extreme_silent(
            values
        ) -> None:
        if ctx.verbose:
            print(Text(" ").debug(title=True), Text("Flag: --extreme-silent").debug(), Text("(full)").valid().italic())
        ctx.log.log("VALID", "Flag", "--extreme-silent activated")
        ctx.silent = 3

    def handle_root(
            values
        ) -> None:
        if ctx.verbose:
            print(Text(" ").debug(title=True), Text("Flag: -r/--root").debug(), Text("(used)").info().italic())

        ctx.root = values[0]
        ctx.log.log("VALID", "Flag", f"-r/--root set to {repr(ctx.root)}")

    def handle_exclude(
            values
        ) -> None:
        if ctx.verbose:
            print(Text(" ").debug(title=True), Text("Flag: -e/--exclude").debug(), Text("(used)").info().italic())

        collected = []
        for v in values:
            if " " in v:
                collected.extend(v.split(" "))
            else:
                collected.append(v)

        if not collected:
            error("-e/--exclude missing values", ctx)

        for path in collected:
            if path not in ctx.exclude:
                ctx.exclude.append(path)

        ctx.log.log("VALID", "Flag", f"-e/--exclude set to {repr(ctx.exclude)}")

    def handle_rule(values) -> None:
        if ctx.verbose:
            print(
                Text(" ").debug(title=True),
                Text("Flag: -R/--rule").debug(),
                Text("(used)").info().italic()
            )

        if len(values) == 0:
            error("-R/--rule requires arguments", ctx)

        if len(values) % 2 != 0:
            error("-R/--rule expects pairs: <CATEGORY> <RULE>", ctx)

        new_rules = {
            "CUSTOM": {
                "name": "Custom Rule Selection",
                "info": "\nRules selected when calling JCCS\n"
            }
        }

        for i in range(0, len(values), 2):
            cat = values[i]
            rule = values[i + 1]

            if cat not in ctx.rules:
                error(f"Category {cat} doesn't exist", ctx)

            if rule not in ctx.rules[cat]:
                error(f"Rule {rule} doesn't exist in {cat}", ctx)

            new_rules["CUSTOM"][rule] = ctx.rules[cat][rule]

        ctx.rules = new_rules

        ctx.log.log("VALID", "Flag", "-R/--rule new rules set")

    def handle_set(values) -> None:
        if ctx.verbose:
            print(
                Text(" ").debug(title=True),
                Text("Flag: -S/--set").debug(),
                Text("(used)").info().italic()
            )

        if len(values) != 4:
            error("-S/--set requires exactly 4 arguments: <CATEGORY> <RULE> <ARG> <VALUE>", ctx)

        cat, rule, varg, val = values

        if cat not in ctx.rules:
            error(f"Category {cat} doesn't exist", ctx)

        if rule not in ctx.rules[cat]:
            error(f"Rule {rule} doesn't exist in {cat}", ctx)

        if varg not in ctx.rules[cat][rule]["arguments"]:
            error(f"{rule} has no argument {varg}", ctx)

        ctx.rules[cat][rule]["arguments"][varg] = val

        ctx.log.log("VALID", "Flag", f"-S set {cat}/{rule}/{varg} to {val}")

    # =========================
    # FLAGS LIST
    # =========================

    FLAGS: list[Flag] = [
        Flag(["-j", "--json-log"], handler=handle_json),
        Flag(["-V", "--verbose"], handler=handle_verbose),
        Flag(["--super-verbose"], handler=handle_super_verbose),

        Flag(["--no-log"], handler=handle_no_log),
        Flag(["--show-log"], handler=handle_show_log),

        Flag(["-s", "--silent"], handler=handle_silent),
        Flag(["--super-silent"], handler=handle_super_silent),
        Flag(["--extreme-silent"], handler=handle_extreme_silent),

        Flag(["-r", "--root"], has_value=True, handler=handle_root),

        Flag(["-e", "--exclude"], has_value=True, multi=True, handler=handle_exclude),

        Flag(["-R", "--rule"], has_value=True, multi=True, handler=handle_rule),

        Flag(["-S", "--set"], has_value=True, multi=True, handler=handle_set),

        # special built-ins
        Flag(["-h"], handler="usage"),
        Flag(["--help"], handler="help"),
        Flag(["-v", "--version"], handler="version"),
        Flag(["-a", "--show-arguments"], handler="arguments"),
        Flag(["--update"], handler="update"),
    ]

    while i < len(argv):
        arg = argv[i]

        if not arg.startswith("-"):
            error(f"invalid argument ({arg})", ctx)

        flag = next((f for f in FLAGS if arg in f.names), None)

        if not flag:
            error(f"invalid flag ({arg})", ctx)
            continue

        # special actions
        if flag.handler == "usage":
            Helper.print_usage(simplename)
            exit(EXIT_SUCCESS)

        if flag.handler == "help":
            Helper.print_help(simplename, fullname, version, author, email)
            exit(EXIT_SUCCESS)

        if flag.handler == "version":
            print(Text(f"{simplename} ({fullname})").bold(), Text(version).italic())
            exit(EXIT_SUCCESS)

        if flag.handler == "arguments":
            Helper.show_arguments(ctx.rules)
            exit(EXIT_SUCCESS)

        if flag.handler == "update":
            update_jccs()
            exit(EXIT_SUCCESS)

        # collect values
        values = []

        if flag.has_value:
            i += 1

            while i < len(argv) and not argv[i].startswith("-"):
                values.append(argv[i])
                i += 1

                if not flag.multi:
                    break

            if not values:
                error(f"missing argument for {arg}", ctx)
        else:
            i += 1

        # call handler
        if callable(flag.handler):
            flag(values)

    return ctx