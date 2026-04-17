#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from types import ModuleType
from typing import Iterable

from program.rule.rule import Rule


class Category:

    def __init__(
            self,
            language: str,
            name: str,
            title: str,
            info: str
        ) -> None:

        if not isinstance(language, str) or not language:
            raise ValueError("Category language must be a non-empty string")

        if not isinstance(name, str) or not name:
            raise ValueError("Category name must be a non-empty string")

        if not isinstance(title, str) or not title:
            raise ValueError("Category title must be a non-empty string")

        if not isinstance(info, str) or not info:
            raise ValueError("Category info must be a non-empty string")

        self.language: str = language
        self.name: str = name
        self.title: str = title
        self.info: str = info
        self.rules: dict[str, Rule] = {}

    def fetch(
            self,
            modules: Iterable[ModuleType]
        ) -> None:

        for module in modules:
            rule = Rule(module)

            # Ensure rule belongs to this category
            if rule.category != self.name:
                raise ValueError(
                    f"Rule '{rule.name}' belongs to category '{rule.category}', "
                    f"cannot be added to '{self.name}'"
                )

            if rule.name in self.rules:
                raise ValueError(
                    f"Duplicate rule '{rule.name}' in category '{self.name}'"
                )

            self.rules[rule.name] = rule

    def __getitem__(
            self,
            name: str
        ) -> Rule:
        if name not in self.rules:
            raise KeyError(
                f"Rule '{name}' not found in category '{self.name}'"
            )

        return self.rules[name]

    def __iter__(
            self
        ) -> Iterable[Rule]:
        return iter(self.rules.values())

    def __len__(
            self
        ) -> int:
        return len(self.rules)

    def __repr__(
            self
        ) -> str:
        return f"<Category {self.name} ({len(self.rules)} rules)>"
