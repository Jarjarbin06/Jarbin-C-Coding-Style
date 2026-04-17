#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_console.ANSI import Color
from jarbin_toolkit_error import Error

from program.helper import get_color

class RuleError(Error):
    """
        RuleError class.

        Rule Error.
    """


    def __init__(
            self,
            error : str = "",
            message : str = "a rule wasn't followed",

            *,
            level : int = -1
        ) -> None:
        """
            Create an Error.

            Parameters:
                error (str, optional) : The error type.
                message (str, optional): The error message.
                link (tuple[str, int | None] | None, optional): The link to where the error comes from (file and line).
        """

        super().__init__(message, error=error)
        self.level = level

    def __str__(
            self,
    ) -> str:
        """
            Get string representation of the error.

            Returns:
                str: String representation of the error.
        """

        reset = Color(Color.C_RESET)

        string: str = ""
        if self.error and self.error.startswith("\n"):
            string += "\n"
        string += f"{get_color(" ", self.level, True) + reset} {get_color("", self.level)}"
        string += (self.error if self.error else "ErrorUnknown").replace("\n", "")
        string += (":" if len(self.message) > 0 else "")

        if len(self.message) > 0:
            string += f"\n{get_color(" ", self.level, True) + reset}"
            for line in self.message.splitlines():
                string += (
                    f"\n"
                    f"{get_color(" ", self.level, True) + reset}"
                    f"     {get_color("", self.level)}"
                )
                string += line

        return string + reset.s
