# JCCS — Jarbin C Coding Style

![JCCS logo failed to load](https://github.com/Jarjarbin06/Jarbin-C-Coding-Style/blob/main/ressources/JCCS_logo.png?raw=true "JCCS logo")

JCCS (Jarbin C Coding Style) is a modular C coding-style checker developed for Epitech projects.
It recursively scans a project directory and validates C source files against a structured, extensible rule system inspired by the official Epitech coding-style specification.

---

## 📌 Overview

JCCS provides:

* Recursive project scanning (hidden files and folders ignored)
* Modular rule system grouped by categories (O, G, MY, etc.)
* Runtime rule selection and dynamic argument overriding
* Structured terminal output with colored results (OK / KO per rule)
* Configurable logging system (JAR-LOG or JSON format)
* Deterministic exit codes for CI and automation workflows
* Built-in verbose and silent execution modes

Each rule is independent and can be executed individually or as part of the full suite.

---

## ⚙️ Program information

Use the following identifiers inside the program:

```
__program__  = "JCCS (Jarbin-C-Coding-Style)"
__version__  = "v0.9"
__author__   = "Jarjarbin06"
__email__    = "nathan.amaraggi@epitech.eu"
```

Console helpers are provided by `jarbin_toolkit_console`.
Logging is handled by `jarbin_toolkit_log` (JAR-LOG or JSON formats).
Execution timing utilities are provided by `jarbin_toolkit_time`.

---

## 📁 Project structure (example)

```
├── epitech_c_coding_style.pdf
├── JCCS
├── LICENSE
├── Makefile
├── README.md
├── ressources
├── scripts
│   ├── install-jccs
│   ├── uninstall-jccs
│   └── update-jccs
└── sources
    ├── JCCS.py
    ├── rules
    │   ├── Rules.py
    │   ├── O
    │   ├── G
    │   └── MY
    └── utils
```

---

## 🧠 Rule system

Rules are registered in `sources/rules/Rules.py`.

The global `RULES` structure is organized as:

* Category key → category metadata + rule entries
* Each rule contains:

  * `"info"` → rule description
  * `"check"` → validation function
  * `"arguments"` → configurable runtime parameters
  * `"level"` → severity (INFO | MINOR | MAJOR | FATAL)

### Rule contract

Each rule must implement:

```
check(paths: list[str], kwargs: dict) -> list[RuleError] | None
```

* `paths`: list of files to analyze
* `kwargs`: runtime parameters (flags + rule arguments)
* returns `None` or empty list if OK, or a list of `RuleError` if violations exist

---

## 🚀 Usage

Run the CLI:

```
JCCS [OPTIONS]
```

### Available options

```
-h, --help
    Display help message and exit.

-v, --version
    Show program name, version and author and exit.

-a, --show-arguments
    Display available categories, rules and their configurable arguments, then exit.

--update
    Update the program and exit.

-r, --root <path>
    Root directory to analyze. Default: current directory (.)

-e, --exclude <path1> [path2 ...]
    Exclude one or several paths from scanning.
    • Accepts space-separated values.
    • Can be used multiple times.
    • Values may also be passed inside quotes.

-R, --rule <rule1> [rule2 ...]
    Run only the specified rule(s).
    • Accepts multiple rule names.
    • Replaces the default rule set with a custom selection.
    • Fails if a rule does not exist.

-S, --set <CATEGORY> <RULE> <ARG> <VALUE>
    Override a rule argument at runtime.
    • CATEGORY must exist.
    • RULE must exist in the category.
    • ARG must be configurable.
    • VALUE replaces the default argument value.

-s, --silent
    Silent mode (level 1): display rule summaries only.

--super-silent
    Silent mode (level 2): display only final JCCS result.

--extreme-silent
    Silent mode (level 3): no output.

-V, --verbose
    Verbose mode (level 1): enable debug output.

--super-verbose
    Verbose mode (level 2): full execution trace output.

-j, --json-log
    Switch log format to JSON (default: JAR-LOG).

--no-log
    Delete log file after execution.

--show-log
    Print generated log at program exit.
```

---

## 🔍 Execution behavior

* Recursively scans all non-hidden files (`.` prefix ignored)
* Traverses directories unless excluded via `--exclude`
* Applies selected rules sequentially by category
* Each rule runs independently with isolated arguments
* Results are displayed as:

  * `[OK]` → no violations
  * `[KO]` → rule violations detected

---

## 📤 Exit codes

```
0   — Success (no style errors found)
84  — Failure (style errors found or invalid usage)
-1  — Fatal internal rule execution error
```

---

## 🛠 Installation

Install system-wide:

```
make install
```

Uninstall:

```
make uninstall
```

Reinstall:

```
make reinstall
```

Update:

```
JCCS --update
```

> [!IMPORTANT]
> While the update script is in the script folder, do not launch it manually, use the command above.

---

## 🧩 Extending JCCS — add a rule

1. Create a new rule file in the correct category folder:

   ```
   sources/rules/<CATEGORY>/<RULE>.py
   ```

2. Implement:

   * `name`
   * `info`
   * `check(paths, kwargs)`
   * optional configurable arguments

3. Register the rule in:

   ```
   sources/rules/Rules.py
   ```

   using:

   * `"info"`
   * `"check"`
   * `"arguments"`
   * `"level"`

Rules must remain deterministic, independent, and side-effect free.

---

## 🎯 Design goals

* Deterministic execution (CI-safe)
* Fully modular rule architecture
* Runtime configurable behavior
* Clear CLI output (OK / KO / errors)
* Flexible logging system (human + machine readable)
* Easy extensibility without core modifications

---

## 📜 License

See the `LICENSE` file included in the repository.

---

## 📎 Notes

* Reference coding-style PDF: `epitech_c_coding_style.pdf`
* Primary target: Epitech C projects
* Rules are extensible for custom project constraints
* Focus on clarity, reproducibility, and strict validation

---

JCCS — Structured. Modular. Deterministic.
