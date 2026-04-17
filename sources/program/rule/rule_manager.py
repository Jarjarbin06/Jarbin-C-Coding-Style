#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from collections.abc import dict_values
from types import ModuleType
from typing import Iterable

from program.rule.category import Category


class RuleManager:

    def __init__(
            self
        ) -> None:
        self.categories: dict[str, Category] = {}

    def add_category(
            self,
            language: str,
            name: str,
            title: str,
            info: str
        ) -> None:
        if name in self.categories:
            raise ValueError(f"Category '{name}' already exists")

        self.categories[name] = Category(language, name, title, info)

    def get_category(
            self,
            name: str
        ) -> Category:
        if name not in self.categories:
            raise KeyError(f"Category '{name}' does not exist")

        return self.categories[name]

    def load_modules(
            self,
            modules: Iterable[ModuleType]
        ) -> None:
        for module in modules:
            # temporary rule to read metadata
            from program.rule.rule import Rule
            rule = Rule(module)

            if rule.category not in self.categories:
                raise ValueError(
                    f"Category '{rule.category}' not registered for rule '{rule.name}'"
                )

            self.categories[rule.category].fetch([module])

    def get_rule(
            self,
            category: str,
            name: str
        ):
        return self.get_category(category)[name]

    def __getitem__(
            self,
            name: str
        ) -> Category:
        return self.get_category(name)

    def __iter__(
            self
        ) -> Iterable[Category]:
        return iter(self.categories.values())

    def __len__(
            self
        ) -> int:
        return len(self.categories)

    def select(
        self,
        pairs: list[tuple[str, str]]
        ) -> "RuleManager":

        new_manager = RuleManager()

        for cat_name, rule_name in pairs:
            if cat_name not in self.categories:
                raise KeyError(f"Category '{cat_name}' does not exist")

            category = self.categories[cat_name]

            if rule_name not in category.rules:
                raise KeyError(
                    f"Rule '{rule_name}' does not exist in '{cat_name}'"
                )

            if cat_name not in new_manager.categories:
                new_manager.categories[cat_name] = Category(
                    category.language,
                    category.name,
                    category.title,
                    category.info
                )

            new_manager.categories[cat_name].rules[rule_name] = category.rules[rule_name]

        return new_manager

    def items(
            self
        ) -> Iterable[tuple[str, Category]]:
        return self.categories.items()

    def values(
            self
        ) -> Iterable[Category]:
        return self.categories.values()

    def keys(
            self
        ) -> Iterable[str]:
        return self.categories.keys()

    def __repr__(
            self
        ) -> str:
        return f"<RuleManager {len(self.categories)} categories>"
