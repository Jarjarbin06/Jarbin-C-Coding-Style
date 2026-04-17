#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from types import ModuleType
from typing import Any, Callable

class Rule:

    def __init__(
            self,
            module: ModuleType
        ) -> None:

        if not isinstance(module, ModuleType):
            raise TypeError("Rule must be initialized with a module")

        self.module = module

        # Required attributes
        self.language: str = self._get_attr("language")
        self.category: str = self._get_attr("category")
        self.name: str = self._get_attr("name")
        self.info: str = self._get_attr("info")
        self.level: int = self._get_attr("level")

        # Required function
        self.check: Callable = self._get_attr("check")

        # Optional custom variables (VAR_*)
        self.variables: dict[str, Any] = self._get_custom_vars()

    def _get_attr(
            self,
            attr: str
        ) -> Any:
        if not hasattr(self.module, attr):
            raise AttributeError(
                f"Rule module '{self.module.__name__}' is missing required attribute '{attr}'"
            )
        return getattr(self.module, attr)

    def _get_custom_vars(
            self
    ) -> dict[str, tuple[Any, str | None]]:
        vars_dict: dict[str, tuple[Any, str | None]] = {}

        for attr in dir(self.module):
            if not attr.startswith("VAR_"):
                continue

            if attr.endswith("_doc"):
                continue

            value = getattr(self.module, attr)

            doc_attr = f"{attr}_doc"

            if hasattr(self.module, doc_attr):
                doc = getattr(self.module, doc_attr)
            else:
                doc = None

            vars_dict[attr] = (value, doc)

        return vars_dict

    def __repr__(
            self
        ) -> str:
        return f"<Rule {self.category}-{self.name} ({self.level})>"
