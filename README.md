# JCCS — Jarbin C Coding Style

JCCS (Jarbin C Coding Style) is a modular C coding-style checker developed for Epitech projects.
It recursively scans a project directory and validates C source files against a structured, extensible rule system inspired by the official Epitech coding-style specification.

---

## 📌 Overview

JCCS provides:

* Recursive project scanning (hidden files and folders ignored)
* Modular rules grouped by categories (easy to add / remove rules)
* Runtime rule selection and per-rule argument overrides
* Structured, colored terminal output and optional JSON or JAR-LOG logging
* Deterministic exit codes for CI and scripting

Each rule is independent and can be executed individually or as part of the full suite.

---

## ⚙️ Program information

Use the following identifiers inside the program:

```
__program__  = "JCCS (Jarbin-C-Coding-Style)"
__version__  = "v0.5"
__author__   = "Jarjarbin06"
__email__    = "nathan.amaraggi@epitech.eu"
```

Console helpers are provided by `jarbin_toolkit_console`. Logging is handled by `jarbin_toolkit_log` (JSON or JAR-LOG).

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
│   └── uninstall-jccs
└── sources
    ├── Error.py
    ├── JCCS.py
    └── rules
        ├── [RULE CATEGORY]
        │   ├── [RULE NAME].py
        │   └── [...]
        ├── [...]
        └── Rules.py
```

---

## 🧠 Rule system

Rules are registered in `sources/rules/Rules.py`. The global `RULES` structure follows:

* Category key -> a mapping with:

  * `"name"`: human readable name
  * `"info"`: description
  * `<RULE_ID>` entries: each rule is a dict with `"info"`, `"check"`, `"arguments"`

Contract for a rule `check` function:

* Signature: `check(files: list[str], kwargs: dict) -> list[RuleError] | None`
* Receives: list of file paths and keyword args (defaults + runtime overrides)
* Returns: `None` or `[]` on success, or a `list[RuleError]` when violations are found

Example conceptual mapping (human-readable):

```
RULES["O"][O1.name] = {
    "info": O1.info,
    "check": O1.check,
    "arguments": {
        "UNAUTHORIZED_EXTENSIONS": O1.UNAUTHORIZED_EXTENSIONS,
        "EXCLUDED_FOLDERS": O1.EXCLUDED_FOLDERS
    }
}
```

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
    • Replaces the default rule set with the custom selection.
    • Fails if a rule does not exist.

-S, --set <CATEGORY> <RULE> <ARG> <VALUE>
    Override a rule argument at runtime.
    • CATEGORY must exist.
    • RULE must exist in the category.
    • ARG must be configurable.

-s, --silent
    Silent mode (level 1): display rule summaries only.

--super-silent
    Silent mode (level 2): display only final JCCS result.

-V, --verbose
    Verbose mode (level 1): enable extra debug output.

--super-verbose
    Verbose mode (level 2): full detailed execution output.

-j, --json-log
    Switch log file format to JSON (default: JAR-LOG).

--no-log
    Delete the log file at program termination.
```

Notes:

* `-e` and `-R` accept multiple space-separated values and can be repeated; quoted groups are also supported.
* `-S` expects four tokens after the flag: `CATEGORY RULE ARG VALUE`.

---

## 🔍 Execution behavior

* Hidden files and folders (starting with `.`) are ignored.
* The tool traverses the root directory recursively; `--exclude` prunes traversal.
* Rules execute sequentially, grouped by category; execution time and logs recorded per rule.
* Rule outputs:

  * `[OK]` — no error
  * `[KO]` — violations found (detailed errors printed unless `--silent`)

---

## 📤 Exit codes

```
0   — Success (no style errors found)
84  — Failure (style errors found or invalid usage)
1   — Fatal internal error during rule execution
```

(Use these codes in CI to differentiate check failures vs internal errors.)

---

## 🛠 Installation

Install system-wide (may require privileges):

```
make install
```

Uninstall:

```
make uninstall
```

Notes:

* Makefile may include targets to install shell completions (Zsh, Bash); check `scripts/`.
* Prefer virtualenv for development.

---

## 🧩 Extending JCCS — add a rule

1. Add a Python module inside the proper category directory (e.g. `sources/rules/G/G7.py`).
2. Implement:

   * `name` (string identifier)
   * `info` (string description)
   * `check(files: list[str], kwargs: dict) -> list[RuleError] | None`
   * optional default argument constants
3. Import and register the rule in `sources/rules/Rules.py` under the right category:

   * Add the rule dict with `"info"`, `"check"` and `"arguments"` entries.

Keep rules single-purpose and deterministic. Use `RuleError` to report violations.

---

## 🎯 Design goals

* Deterministic, reproducible behavior (CI-ready)
* Modular rule architecture — easy to extend and maintain
* Clear exit codes and structured output
* Configurable logging (human or JSON)
* Readable output and developer-friendly internals

---

## 📜 License

See the `LICENSE` file included in the repository.

---

## 📎 Notes

* Reference coding-style PDF: `epitech_c_coding_style.pdf` (included)
* Primary target: Epitech C projects; rules are reusable
* Focus: clarity, maintainability, predictable results

---

JCCS — Structured. Modular. Deterministic.
<small>Readme made with AI</small>
