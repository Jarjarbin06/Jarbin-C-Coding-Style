#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_error import Error

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
            link : tuple[str , int | None] | None = None,
            level : str = "INFO"
        ) -> None:
        """
            Create an Error.

            Parameters:
                error (str, optional) : The error type.
                message (str, optional): The error message.
                link (tuple[str, int | None] | None, optional): The link to where the error comes from (file and line).
        """

        super().__init__(message, error=error, link=link)
        if level == "FATAL":
            self.level_color = 95
        elif level == "MAJOR":
            self.level_color = 91
        elif level == "MINOR":
            self.level_color = 93
        elif level == "INFO":
            self.level_color = 96
        else:
            self.level_color = 97

    def __str__(
            self,
    ) -> str:
        """
            Get string representation of the error.

            Returns:
                str: String representation of the error.
        """

        string: str = ""
        if self.error and self.error.startswith("\n"):
            string += "\n"
        string += f"\x1b[{self.level_color + 10}m \x1b[0m \x1b[{self.level_color}m"
        string += (self.error if self.error else "ErrorUnknown").replace("\n", "")
        string += (":" if len(self.message) > 0 else "")

        if len(self.message) > 0:
            for line in self.message.splitlines():
                string += f"\n\x1b[{self.level_color + 10}m \x1b[0m     \x1b[{self.level_color}m"
                string += line

        string += (f"\n\x1b[{self.level_color + 10}m \x1b[0m \x1b[{self.level_color}m" + f"\x1b[{self.level_color + 10}m \x1b[0m\n\x1b[{self.level_color + 10}m \x1b[0m  \x1b[{self.level_color}m" + self.link) if self.link else ""

        return string
