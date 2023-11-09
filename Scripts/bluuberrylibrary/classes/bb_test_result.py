"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.classes.bb_run_result import BBRunResult
from event_testing.results import TestResult


class BBTestResult(BBRunResult):
    """BBTestResult(\
        result,\
        reason,\
        tooltip_text=None,\
        icon=None,\
        influence_by_active_mood=False\
    )

    The result of a test.

    :param result: True, if the test was successful. False, if unsuccessful.
    :type result: bool
    :param reason: The reason for the test result.
    :type reason: str
    :param tooltip_text: The text to show if the result is returned to a UI Element.
    :type tooltip_text: Any, optional
    :param icon: The icon to show with the result.
    :type icon: Any, optional
    :param influence_by_active_mood: True, if the result was influenced by the active Mood of a Sim. Default is False.
    :type influence_by_active_mood: bool, optional
    """
    TRUE = None
    FALSE = None
    NONE = None

    def __init__(
        self,
        result: bool,
        reason: str,
        tooltip_text: Any = None,
        icon: Any = None,
        influence_by_active_mood: bool = False
    ):
        super().__init__(
            result,
            reason,
            tooltip_text=tooltip_text,
            icon=icon,
            influence_by_active_mood=influence_by_active_mood
        )

    @classmethod
    def from_base(cls, test_result: TestResult) -> 'BBTestResult':
        """from_base(test_result)

        Convert a TestResult into a BBTestResult.

        :param test_result: The TestResult to convert.
        :type test_result: TestResult
        :return: A BBTestResult
        :rtype: BBTestResult
        """
        return BBTestResult(
            test_result.result,
            test_result.reason,
            tooltip_text=test_result.tooltip,
            icon=test_result.icon,
            influence_by_active_mood=test_result.influence_by_active_mood
        )

    def reverse(self) -> 'BBTestResult':
        """reverse()

        Flip the result of this TestResult and return a new BBTestResult.

        :return: A new Test Result, but with a reversed "result" value.
        :rtype: BBTestResult
        """
        return BBTestResult(
            not self.result,
            self.reason,
            tooltip_text=self._tooltip_text,
            icon=self.icon,
            influence_by_active_mood=self.influence_by_active_mood
        )

    def __str__(self):
        if self.reason:
            return self.reason
        return str(bool(self.result))

    def __repr__(self):
        if self.reason:
            return '<BBTestResult: {0} ({1})>'.format(bool(self.result), self.reason)
        return '<BBTestResult: {0}>'.format(bool(self.result))

    def __eq__(self, other):
        if isinstance(other, BBTestResult):
            return self.result == other.result
        return super().__eq__(other)

    def __and__(self, other):
        result = self.result and other.result
        tooltip = self._tooltip_text or other._tooltip_text if hasattr(other, '_tooltip_text') else other.tooltip
        # noinspection PyUnresolvedReferences
        if self._reason:
            # noinspection PyUnresolvedReferences
            reason = self._reason
        else:
            reason = other._reason
        if result:
            icon = self.icon or other.icon
            influence_by_active_mood = self.influence_by_active_mood or other.influence_by_active_mood
        else:
            icon = None
            influence_by_active_mood = False
        return BBTestResult(result, reason, tooltip_text=tooltip, icon=icon, influence_by_active_mood=influence_by_active_mood)


BBTestResult.TRUE = BBTestResult(True, 'Success')
BBTestResult.FALSE = BBTestResult(False, 'Failure')
BBTestResult.NONE = BBTestResult(False, 'Failure')
