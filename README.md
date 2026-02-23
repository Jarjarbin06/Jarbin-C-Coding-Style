# JCCS — Jarbin C Coding Style


JCCS (Jarbin C Coding Style) is a modular C coding style checker designed for Epitech projects.  
It analyzes a project directory and validates C source files against a structured rule system inspired by the official coding style specification.

---

## 📌 Overview

JCCS is built to:

- Recursively scan a project directory
- Apply configurable coding style rules
- Support rule filtering and runtime argument configuration
- Provide structured and colored terminal output
- Return standardized exit codes for scripting and CI integration

The checker is fully modular: each rule is independent and can be executed individually.

---

## ⚙️ Program Information

```text
__program__ = "JCCS (Jarbin-C-Coding-Style)"
__version__ = "v0.2"
__author__ = "Jarjarbin06"
__email__ = "nathan.amaraggi@epitech.eu"
```

---

## 📁 Project Structure

```text
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

## 🧠 Rule System

Rules are registered inside:

```text
sources/rules/Rules.py
```

Each rule is declared inside the global `RULES` dictionary:

```text
RULES["RULE-ID"] = {
    "info": <rule_description>,
    "check": <rule_function>,
    "arguments": {
        "ARG_NAME": <argument_default_value>
    }
}
```

### Example — C-O1

```text
RULES["C-O1"] = {
    "info": O1.info,
    "check": O1.check,
    "arguments": {
        "UNAUTHORIZED_EXTENSIONS": O1.UNAUTHORIZED_EXTENSIONS,
        "EXCLUDED_FOLDERS": O1.EXCLUDED_FOLDERS
    }
}
```

Each rule:

- Receives a list of file paths
- Returns a list of `RuleError` objects if violations are found
- Can optionally support verbose mode

---

## 🚀 Usage

```text
JCCS [OPTIONS]
```

### Available Options

```text
-h, --help
    Display help message and exit.

-v, --version
    Show program name, version and author and exit.

-r, --root <path>
    Define the root directory to analyze.
    Default: current directory (.)

-e, --exclude <path>
    Define the root directory to analyze.
    Default: current directory (.)

-R, --rule <rule_name>
    Run only a specific rule.

-R, --rule "[RULE1 RULE2 ...]"
    Run multiple specific rules (space separated inside brackets).

-S, --set <CATEGORY> <RULE> <ARG> <VALUE>
    Override a rule argument at runtime.

-a, --show-arguments
    Display all available rules and their configurable arguments and exit.

-s, --silent
    Display only JCCS result and rule summaries (hide detailed error output).

--super-silent
    Display only JCCS result (hide detailed error output and summaries).

-V, --verbose
    Enable minimal verbose mode for supported rules.

--super-verbose
    Enable full verbose mode for supported rules.
```

---

## 🔍 Execution Behavior

- Hidden files and folders are ignored.
- The root directory is scanned recursively.
- Rules are executed sequentially.
- Each rule outputs:
  - `[OK]` if no error
  - `[KO]` if violations detected
- Detailed errors are printed unless `--silent` is enabled.

---

## 📤 Exit Codes

```text
0       Success (no style errors found)
84      Failure (style errors detected or invalid usage)
-1      Fatal internal rule execution error
```

---

## 🛠 Installation

To install:

```text
make install
```

To uninstall:

```text
make uninstall
```

---

## 🧩 Extending JCCS

To create a new rule:

1. Add a Python file inside the appropriate category folder.
2. Implement:
   - `info` (string description)
   - `check(files: list[str], kwargs: dict) -> list[RuleError] | None`
3. Register it in `Rules.py`.

The architecture ensures:

- Strict separation between rules
- Centralized rule management
- Runtime argument configurability

---

## 🎯 Design Goals

- Deterministic and predictable behavior
- Modular rule architecture
- Strict exit code policy
- CI/CD compatible
- Clean and structured output
- Easily extensible for future rule sets

---

## 📜 License

See the `LICENSE` file for details.

---

## 📎 Notes

- The reference coding style specification is provided in:
  
```text
epitech_c_coding_style.pdf
```

- Designed primarily for Epitech C projects.
- Built with clarity, structure, and maintainability in mind.

---

**JCCS — Structured. Modular. Deterministic.**
