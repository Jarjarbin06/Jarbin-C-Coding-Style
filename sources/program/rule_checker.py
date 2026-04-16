#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from sys import stderr
from typing import Callable, Any
import jarbin_toolkit_console as Console
import jarbin_toolkit_time as Time
from jarbin_toolkit_log import Log

from utils.error import RuleError

print = Console.Console.print
Text = Console.Text.Text
Color = Console.ANSI.Color
Cursor = Console.ANSI.Cursor

Console.init(banner=False)

def check(
        rules: dict[str, str | dict[str, str | dict[str, str | Callable | dict[str, Any]]]],
        paths: list[str],
        log: Log,
        root: str = ".",
        silent: int = 0,
        verbose: int = 0
    ) -> int:

    def get_color(text: str) -> Text:
        level = rules[category][rule]["level"]

        if level == "FATAL":
            level_color = 95
        elif level == "MAJOR":
            level_color = 91
        elif level == "MINOR":
            level_color = 93
        elif level == "INFO":
            level_color = 96
        else:
            level_color = 97

        return Text(Color(level_color) + text)

    log_type = log.log_file_type

    errors: list[RuleError]
    category_error_count: int
    keywords_args: dict
    len_title_line: int
    rule_time: float
    show_category_boxes: bool = silent < 2
    show_rule_errors: bool = silent == 0
    jccs_timer: Time.StopWatch = Time.StopWatch()
    category_timer: Time.StopWatch = Time.StopWatch()
    rule_timer: Time.StopWatch = Time.StopWatch()
    error_count: int = 0
    args: list = paths
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
        len_title_line = len(f"┏━ {rules[category]["name"]} {"━" * 5} [•STARTED•] ━┓")

        if show_category_boxes:
            print("┏━", Text(f"{rules[category]["name"]}").bold(), "━" * 5, Text("[•STARTED•]").valid(), "━┓")
            print(Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃"), end="\n")

        for rule in rules[category]:
            if rule in ["name", "info"]:
                continue

            try:
                log.log("INFO", f"Rule {rule}", f"entering rule {repr(rule)}")
                if log_type == "jar-log":
                    log.comment(f"{rule} rule info:{rules[category][rule]["info"].removesuffix("\n")}")

                keywords_args = {}

                for arg in rules[category][rule]["arguments"]:
                    keywords_args[arg] = rules[category][rule]["arguments"][arg]

                keywords_args["verbose"] = verbose
                keywords_args["root"] = root

                log.log("INFO", f"Rule {rule}", f"**kwargs set")
                if log_type == "jar-log":
                    log.comment(f"**kwargs = {repr(keywords_args)}")

                log.log("INFO", f"Rule {rule}", f"launching {repr(rule)} rule check")
                rule_timer.start()

                errors = rules[category][rule]["check"](args, kwargs=keywords_args)

                rule_time = rule_timer.elapsed()
                log.log("INFO", f"Rule {rule}", f"ending {repr(rule)} rule check")

                if verbose:
                    print(Text(" ").debug(title=True), Text(f"elapsed time for {category}/{rule} : {rule_time}").debug())

                if log_type == "jar-log":
                    log.comment(f"elapsed time for {category}/{rule} : {rule_time:.5f}")

                rule_timer.reset()

                if errors:

                    log.log("INFO", f"Rule {rule}", f"errors found ({len(errors)} errors)")
                    category_error_count += len(errors)

                    if show_category_boxes:
                        print(get_color("┃"), get_color(rule).bold(), get_color(f"({len(errors)})").italic(), end="")
                        print(Cursor.move_column(len_title_line - 6) + get_color("[KO]"), get_color(" ┃"), get_color(f"◀ {rules[category][rule]["level"]}"), end=("\n" + str(get_color("┃")) + "\n" if show_rule_errors else "\n"))

                    for rule_error in errors:
                        log.log("ERROR", f"Rule {rule}", f"{rule_error.message.split("\n")[0]}")

                        if show_rule_errors:
                            print(get_color("┃ ") + str(rule_error).replace("\n", str(Color(Color.C_RESET) + "\n" + get_color("┃ "))), end=get_color("┃\n") + Color(Color.C_RESET), file=stderr)


                elif show_category_boxes:
                    print(Text("┃"), Text(f"{rule}").bold(), Text("(no error)").italic(), end="")
                    print(Cursor.move_column(len_title_line - 6) + Text("[OK]").valid(), Text(" ┃"), end=("\n" if show_rule_errors else "\n"))

                log.log("INFO", f"Rule {rule}", f"leaving rule {repr(rule)}")

            except BaseException as err:

                log.log("CRIT", f"Rule {rule}", f"{str(err)}")

                if show_category_boxes:
                    print(Text("┃"), Text(f"{rule} [FATAL ERROR]").critic(), file=stderr)
                    print(Text("┃"), Text(f"terminating JCCS").error(), file=stderr)
                    print("┗━", Text(f"{rules[category]["name"]} ").bold(), "━" * 5, Text("[••TERM••]").critic(), "━┛", end="\n\n")
                return -1

        if show_category_boxes:
            print(Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃"), end="\n")
            print("┗━", Text(f"{rules[category]["name"]}").bold(), "━" * 5, (Text("[••ENDED••]").error() if category_error_count else Text("[••ENDED••]").valid()), "━┛", end="\n\n")

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
