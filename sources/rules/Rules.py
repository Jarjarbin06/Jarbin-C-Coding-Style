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

RULE_MANAGER = RuleManager()
ERRORS: list[str] = []


# =========================
# CATEGORY REGISTRATION
# =========================
def register_category(
    key: str,
    language: str,
    name: str,
    title: str,
    info: str,
    modules: list
) -> None:
    try:
        RULE_MANAGER.add_category(language, name, title, info)

        category = RULE_MANAGER.get_category(name)
        category.fetch(modules)

    except BaseException as e:
        ERRORS.append(f"{key} rules ({name}) → {e}")


# =========================
# C-O — FILE ORGANIZATION
# =========================
try:
    from rules.O import O1, O2, O3, O4

    register_category(
        "O",
        "C",
        "O",
        "Files Organization",
        """Keep repository clean and structured.
Avoid compiled, temporary, or unnecessary files.
Use correct naming conventions and limit complexity per file.""",
        [O1, O2, O3, O4]
    )

except BaseException as e:
    ERRORS.append(f"O rules (C-O) → {e}")


# =========================
# C-G — GLOBAL SCOPE
# =========================
try:
    from rules.G import G1, G2, G3, G4, G5, G6, G7, G8, G9, G10

    register_category(
        "G",
        "C",
        "G",
        "Global Scope",
        """Enforces coding style rules for global scope usage, formatting,
headers, includes, and structural constraints.""",
        [G1, G3, G4, G5, G6, G7, G8, G9, G10]
    )

except BaseException as e:
    ERRORS.append(f"G rules (C-G) → {e}")


# =========================
# CUSTOM RULES
# =========================
try:
    from rules.MY import JCCS1, JCCS2

    register_category(
        "JCCS",
        "Any",
        "JCCS",
        "Custom Rules",
        """Rules not in the 'Epitech C Coding Style' that can be useful.""",
        [JCCS1, JCCS2]
    )

except BaseException as e:
    ERRORS.append(f"MY rules → {e}")


# =========================
# DEBUG OUTPUT
# =========================
if ERRORS:
    for err in ERRORS:
        print(Text(err).error())


Console.quit(delete_log=True)
