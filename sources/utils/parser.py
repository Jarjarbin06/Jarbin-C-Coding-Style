#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

import re

class Parser:

    class C:

        RE_FUNCTION_CALL_PATTERN = re.compile(
            r'(?<![a-zA-Z0-9_])([a-zA-Z_]\w*)\s*\('
        )
        RE_INCLUDE_PATTERN = re.compile(
            r'#include\s*[<"]([^">]+)[">]'
        )
        RE_HEADER_C_PATTERN = re.compile(
            r"/\*\s*\n"
            r"\*\* EPITECH PROJECT, \d{4}\s*\n"
            r"\*\* .+?\s*-\s*.+\s*\n"
            r"\*\* File description:\s*\n"
            r"(?:\*\* .+\s*\n)*"
            r"\*/",
            re.DOTALL
        )
        RE_GLOBAL_VAR_PATTERN = re.compile(
            r'^(?!.*\bconst\b)(?!.*\bstatic\b)(?!.*\btypedef\b)'
            r'\s*[a-zA-Z_]\w*\s+[a-zA-Z_]\w*\s*(=|;)',
            re.MULTILINE
        )

        @staticmethod
        def extract_function_calls(content: str) -> list[str]:
            return Parser.C.RE_FUNCTION_CALL_PATTERN.findall(content)

        @staticmethod
        def extract_includes(content: str) -> list[str]:
            match = Parser.C.RE_INCLUDE_PATTERN.search(content)
            return [match.group(1)] if match else []

        @staticmethod
        def has_c_header(content: str) -> bool:
            return Parser.C.RE_HEADER_C_PATTERN.search(content) is not None

        @staticmethod
        def extract_potential_globals(content: str) -> list[str]:
            return Parser.C.RE_GLOBAL_VAR_PATTERN.findall(content)

    class Makefile:
        RE_HEADER_MAKEFILE_PATTERN = re.compile(
            r"##\s*\n"
            r"## EPITECH PROJECT, \d{4}\s*\n"
            r"## .+?\s*-\s*.+\s*\n"
            r"## File description:\s*\n"
            r"(?:## .+\s*\n)*"
            r"##\s*\n",
            re.DOTALL
        )

        @staticmethod
        def has_makefile_header(content: str) -> bool:
            return Parser.Makefile.RE_HEADER_MAKEFILE_PATTERN.search(content) is not None
