from typing import List, Dict

from mcmd.script.model.lines import ParsedLine, Line
from mcmd.script.parser.errors import ScriptValidationError


class _ParseState:

    def __init__(self):
        self.lines: List[ParsedLine] = list()
        self.raw_lines: List[str] = list()
        self.combined_lines: List[Line] = list()
        self.required_args: Dict[int, str] = dict()
        self.errors: List[ScriptValidationError] = list()
