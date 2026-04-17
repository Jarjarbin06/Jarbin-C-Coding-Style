Here is your **cleaned, reformatted, more readable README** with the corrected section integrated and structure improved (no logic changes, only clarity + presentation + consistency):

---

# JCCS — Rule Creation & Indexing Guide

This document explains how to create a rule using the standard template and how to register it inside the JCCS rule indexer.

---

# 1. Rule Template (Standard Format)

Every rule in JCCS must follow this structure:

```python
#############################
###         JCCS          ###
#############################

# INFO #
language = "L"
category = "C"
name = f"{category}R"

info = f"""
{language}-{name} - Rule title
Short description of the rule behavior.
"""

level = "LVL"
```

### Meaning

* `L` → language (`C`, `PY`, etc.)
* `C` → category
* `R` → rule number
* `LVL` → severity level (`INFO`, `MINOR`, `MAJOR`, `FATAL`)

---

# 2. Required Imports

Every rule must include:

```python
import re
import jarbin_toolkit_console as Console

from utils.error import RuleError
from utils.file import File
from utils.transform import Transform
from utils.format import Format

print = Console.Console.print
Text = Console.Text.Text
```

---

# 3. Custom Variables

Rules can define configurable parameters:

```python
VAR_MY_VAR = ""
VAR_MY_VAR_doc = "Short description of this variable."
```

Every custom variables have to start with `VAR_`.\
These values can be overridden at runtime via `-S / --set`.

---

# 4. Regex Handling

All pattern matching must use precompiled regex:

```python
RE_MY_PATTERN = re.compile(r"...")
```

✔ Avoid compiling regex inside loops
✔ Keep patterns reusable and global

---

# 5. Content Checker (CORE LOGIC)

All file analysis must be isolated in this function:

```python
def get_content_error(file: str) -> str:
    """
    File content analysis only (NO path logic here)
    """

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    for i, line in cleaned:

        stripped = line.strip()
        if not stripped:
            continue

        if RE_MY_PATTERN.search(line):

            return Format.error(
                i,
                line.rstrip("\n"),
                "rule violation detected"
            )

    return ""
```

### Rules

* NO path handling
* NO extension filtering
* ONLY content analysis
* Must return:

  * formatted error OR
  * empty string

---

# 6. Main Check Function

```python
def check(paths, **kwargs) -> list[RuleError] | None:
```

### 6.1 Extract arguments

```python
kwargs = kwargs["kwargs"]
verbose = kwargs.get("verbose", 0)
```

---

### 6.2 Override custom variables

```python
global MY_VAR
MY_VAR = kwargs.get("MY_VAR", MY_VAR)

if isinstance(MY_VAR, tuple):
    MY_VAR = MY_VAR[0]
```

---

# 7. File Filtering Rules (IMPORTANT)

File filtering is **NOT global**.

Each rule defines its own scope.

---

## 7.1 Core principle

👉 The rule decides what it checks
👉 The engine does NOT pre-filter logic

---

## 7.2 Example patterns

### ✔ C-only rule

```python
if not file.endswith(".c"):
    return True
```

---

### ✔ C + header rule

```python
if not (file.endswith(".c") or file.endswith(".h")):
    return True
```

---

### ✔ No filtering (all files)

```python
# rule applies to every file
```

---

### ✔ Folder-based exclusion

```python
if "/tests/" in file:
    return True
```

---

## 7.3 Design rule

Every rule must clearly define:

* its scope (what it checks)
* what it ignores
* why it ignores it

---

# 8. Error Handling Pattern

```python
if get_content_error(file):
    return False
```

---

# 9. Main Loop Pattern

```python
for file in paths:
    try:
        assert check_file(file), (
            f"{file}\n"
            "Rule violation detected\n\n"
            f"{get_content_error(file)}"
        )

    except AssertionError as error:
        errors.append(RuleError(f"{category}-{name}", str(error), level=level))
```

---

# 10. Logging (Verbose Mode)

### Start

```python
if verbose:
    print(
        Text(" ").debug(title=True),
        Text(f"C-{name}: starting check").debug()
    )
```

---

### End

```python
if verbose:
    print(
        Text(" ").debug(title=True),
        Text(f"C-{name}: ending check").debug(),
        Text(f"({len(errors)} errors found)").error().italic()
        if errors else Text("(no error)").valid().italic()
    )
```

---

# 11. Final Return

```python
return errors if errors else None
```

---

# 12. Registering a Rule in the Indexer

Rules must be imported and registered manually.

---

## 12.1 Import

```python
from rules.G import G10
```

---

## 12.2 Register rule

```python
RULES[category][name] = {
    "info": info,
    "check": check_function,
    "arguments": {},
    "level": level
}
```

---

# 13. Rule Arguments

Rules can expose configurable parameters:

```python
"arguments": {
    "MY_VAR": (MY_VAR, MY_VAR_doc)
}
```

---

### Example (real case)

```python
RULES["G"][G9.name] = {
    "info": G9.info,
    "check": G9.check,
    "arguments": {
        "AUTHORIZED_VALUES": (G9.AUTHORIZED_VALUES, G9.AUTHORIZED_VALUES_doc)
    },
    "level": G9.level
}
```

---

# 14. Category Structure

Rules are grouped by category:

| Category | Meaning            |
|----------|--------------------|
| O        | Files organization |
| G        | Global scope rules |
| MY       | Custom rules       |

---

### Category format

```python
RULES["X"] = {
    "name": "...",
    "info": "..."
}
```

---

# 15. Summary

To create a rule:

1. Copy template
2. Define variables
3. Add regex
4. Implement `get_content_error`
5. Implement `check`
6. Add logging
7. Register in indexer

---

If you want next step, I can help you design:

* rule priority system
* parallel execution engine
* caching system
* or AST-based analysis engine (big upgrade for JCCS)
