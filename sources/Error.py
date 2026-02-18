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
            link : tuple[str , int | None] | None = None
        ) -> None:
        """
            Create an Error.

            Parameters:
                error (str, optional) : The error type.
                message (str, optional): The error message.
                link (tuple[str, int | None] | None, optional): The link to where the error comes from (file and line).
        """

        self.message : str = message
        self.error : str = error
        self.link_data : tuple[str, int] | None = link
        self.link : str | None = None

        self.create_link()
        self.log()