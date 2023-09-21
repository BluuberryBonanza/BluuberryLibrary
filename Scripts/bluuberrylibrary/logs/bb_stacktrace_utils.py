"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import sys
import traceback
from collections import namedtuple
from typing import Any, List

# The following was tweaked slightly from the publicly made available, copyright free code here: https://stackoverflow.com/questions/13210436/get-full-traceback
FullTraceback = namedtuple('FullTraceback', ('tb_frame', 'tb_lineno', 'tb_next'))


class BBStacktraceUtils:
    """Utilities for accessing the stack trace of your mod.

    """
    @classmethod
    def current_stack(cls, skip_lines: int = 1) -> Any:
        """current_stack(skip_lines=1)

        Retrieve the current stack

        :param skip_lines: The number of lines to skip. Default is 1.
        :type skip_lines: int, optional
        :return: A collection of the current stack.
        """
        cur_frame = None
        try:
            1/0
        except ZeroDivisionError:
            # noinspection PyUnresolvedReferences
            cur_frame = sys.exc_info()[2].tb_frame
        for i in range(skip_lines + 2):
            cur_frame = cur_frame.f_back
        stack_trace = []
        while cur_frame is not None:
            stack_trace.append((cur_frame, cur_frame.f_lineno))
            cur_frame = cur_frame.f_back
        return stack_trace

    @classmethod
    def get_full_stack_trace(cls, skip_lines: int = 1) -> List[str]:
        """Retrieve the full stacktrace from the current stack.

        :return: A list of stack trace lines.
        :rtype: List[str]
        """
        exception_type, exception_value, exception_traceback = sys.exc_info()
        current_stack = cls.current_stack(skip_lines=skip_lines)
        full_traceback = exception_traceback
        for (traceback_frame, traceback_line_number) in current_stack:
            full_traceback = FullTraceback(traceback_frame, traceback_line_number, full_traceback)
        # noinspection PyTypeChecker
        return traceback.format_exception(
            exception_type,
            exception_value,
            full_traceback
        )
