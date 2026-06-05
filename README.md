![JCCS logo failed to load](https://github.com/Jarjarbin06/Jarbin-C-Coding-Style/blob/main/ressources/JCCS_logo.png?raw=true "JCCS logo")

# 📦 JCCS — Jarbin C Coding Style

> Modular and deterministic C coding-style checker designed for EPITECH projects, providing recursive analysis, rule-based validation, and CI-friendly execution.

---

## 🔹 Short Description

**JCCS is a structured C coding-style validation tool that scans project directories and enforces rules based on a modular, extensible system inspired by the EPITECH coding-style specification.**

It provides a flexible CLI, configurable rule execution, and deterministic outputs suitable for automation and continuous integration.

---

## 🔹 Authors

* Nathan (Jarjarbin06)
* EPITECH Project

---

## 🔹 License

GPL v3

---

## 🔹 Target Audience

JCCS is designed for:

* EPITECH students validating coding-style compliance
* C developers enforcing strict style rules
* CI/CD pipelines requiring deterministic validation tools
* Projects needing modular and extensible rule systems
* Developers building custom coding-style extensions

---

## 🔹 Platform Support

* Linux compatible
* Python-based execution
* No OS-specific dependencies beyond standard environment
* CLI-oriented usage

---

## 🔹 Purpose

JCCS aims to replace manual coding-style verification (and `epiclang`) by providing:

* Recursive project scanning (excluding hidden files)
* Modular rule-based validation system
* Runtime rule selection and configuration
* Deterministic execution for CI pipelines
* Structured logging (JAR-LOG or JSON)
* Clear OK / KO rule reporting
* Multiple verbosity levels

It is **not a formatter**, but a **strict validation tool**.

---

## 🔹 Key Features

* Recursive directory scanning
* Modular rule system (categories: O, G, MY, etc.)
* Independent rule execution
* Runtime argument overriding (`--set`)
* Selective rule execution (`--rule`)
* Structured colored output (OK / KO)
* Multi-level verbosity and silent modes
* JSON and JAR-LOG logging formats
* Deterministic exit codes for automation
* Built-in update system

---

## 🔹 Architecture Overview

```
        ┌──────────────────────────┐
        │     CLI Interface        │
        │     (JCCS command)       │
        └────────────┬─────────────┘
                     │
                     ▼

        ┌──────────────────────────┐
        │  Project Scanner         │
        │ (recursive traversal)    │
        └────────────┬─────────────┘
                     │
                     ▼

        ┌──────────────────────────┐
        │   Rule Dispatcher        │
        │ (category-based system)  │
        └────────────┬─────────────┘
                     │
 ┌───────────────────┼───────────────────┼───────────────┐
 │                   │                   │               │
┌────────────────┐  ┌────────────────┐  ┌────────────┐  ┌─────┐
│ Rule O         │  │ Rule G         │  │ Rule JCCS  │  │ ... │
│ (Organization) │  │ (Global scope) │  │ (Custom)   │  │ ... │
└────────────────┘  └────────────────┘  └────────────┘  └─────┘


    │
    ▼
┌──────────────────────────┐
│ Output / Logging System  │
│ (OK / KO + logs)         │
└──────────────────────────┘
```

---

## 🔹 Core Concept

JCCS is based on a **modular rule execution system**:

* Rules are grouped by **categories**
* Each rule is **independent and deterministic**
* Rules receive:

  * file paths
  * runtime arguments

---

### Rule contract

```python
check(paths: list[str], kwargs: dict) -> list[RuleError] | None
````

* `paths` → files to analyze
* `kwargs` → runtime configuration
* returns:

  * `None` or empty → OK
  * list of errors → KO

---

## 🔹 Project Structure

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
    │   └── JCCS
    └── utils
```

---

## 🔹 CLI Usage

### Basic command

```bash
JCCS [OPTIONS]
```

---

### Core Options

```bash
-h, --help
-v, --version
-a, --show-arguments
--update
```

---

### Execution Control

```bash
-r, --root <path>
-e, --exclude <path...>
-R, --rule <rule...>
-S, --set <CATEGORY> <RULE> <ARG> <VALUE>
```

---

### Output Modes

```bash
-s, --silent
--super-silent
--extreme-silent
```

---

### Verbosity

```bash
-V, --verbose
--super-verbose
```

---

### Logging

```bash
-j, --json-log
--no-log
--show-log
```

---

## 🔹 Execution Behavior

* Recursively scans project directory
* Ignores hidden files and folders
* Applies rules sequentially
* Each rule executes independently
* Output format:

```
[OK] → no violations
[KO] → violations detected
```

---

## 🔹 Exit Codes

```
0   → Success (no errors)
84  → Style errors or invalid usage
-1  → Internal rule failure
```

---

## 🔹 Installation

### Install

```bash
make install
```

### Uninstall

```bash
make uninstall
```

### Reinstall

```bash
make reinstall
```

### Update

```bash
JCCS --update
```

> [!IMPORTANT]
> While the update script is in the script folder, do not launch it manually, use the command above.

---

## 🔹 Rule System

Rules are defined in:

```
sources/rules/Rules.py
```

Each rule contains:

* `info` → description
* `check` → validation function
* `arguments` → configurable parameters
* `level` → severity

---

## 🔹 Extending JCCS

### Add a new rule

1. Create:

```
sources/rules/<CATEGORY>/<RULE>.py
```

2. Implement:

* rule name
* `check()` function
* optional arguments

3. Register in:

```
sources/rules/Rules.py
```

---

### Constraints

* Rules must be deterministic
* No side effects allowed
* Independent execution only

---

## 🔹 Memory & Execution Model

* No persistent state between rules
* File list shared across rules
* Arguments passed per rule execution
* Logging system isolated from rule logic

---

## 🔹 Design Philosophy

* Deterministic execution (CI-safe)
* Modular and extensible architecture
* Strict validation (no auto-fix)
* Clear and structured output
* Runtime configurability
* Separation of concerns (rules vs engine)

---

## 🔹 Current State

⚠️ Stable and actively evolving

Status:

* Recursive scanning implemented
* Rule system fully modular
* CLI fully functional
* Logging system operational
* Runtime configuration supported

Limitations:

* No automatic formatting
* Depends on rule completeness
* Performance scales with project size (still fast for 20000+ files)
* No parallel execution (yet)

---

## 🔹 File Structure

```
sources/    → Core implementation
rules/      → Rule definitions
utils/      → Helpers and tooling
scripts/    → Install / update tools
```

---

## 🔹 Notes

* Based on EPITECH coding-style philosophy
* Designed for strict validation workflows
* Easily extensible for custom rules
* Suitable for CI/CD pipelines
* Focus on reproducibility and clarity

---

JCCS — Structured. Modular. Deterministic.
