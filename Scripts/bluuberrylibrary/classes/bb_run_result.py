"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils

# noinspection PyBroadException
try:
    from event_testing.results import TestResult
except:
    class TestResult:
        def __init__(
            self,
            result: Any,
            reason: str,
            tooltip: Any = None,
            icon: Any = None,
            influence_by_active_mood: bool = False
        ):
            self.result = result
            self.reason = reason
            self.tooltip = tooltip
            self.icon = icon
            self.influence_by_active_mood = influence_by_active_mood


class BBRunResult(TestResult):
    """BBRunResult(\
        result,\
        reason,\
        tooltip_text=None,\
        icon=None,\
        influence_by_active_mood=False\
    )

    The result of running something.

    :param result: The result of execution. Whether this is an Object, a Boolean, or some other Type.
    :type result: Any
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
        result: Any,
        reason: str,
        tooltip_text: Any = None,
        icon: Any = None,
        influence_by_active_mood: bool = False
    ):
        self._tooltip_text = tooltip_text
        if tooltip_text is not None:
            tooltip_text = BBLocalizationUtils.to_localized_tooltip(tooltip_text)
        super().__init__(
            result,
            reason,
            tooltip=tooltip_text,
            icon=icon,
            influence_by_active_mood=influence_by_active_mood
        )

    @classmethod
    def from_base(cls, test_result: TestResult) -> 'BBRunResult':
        """from_base(test_result)

        Convert a TestResult into a BBRunResult.

        :param test_result: The TestResult to convert.
        :type test_result: TestResult
        :return: A BBRunResult
        :rtype: BBRunResult
        """
        return BBRunResult(
            test_result.result,
            test_result.reason,
            tooltip_text=test_result.tooltip,
            icon=test_result.icon,
            influence_by_active_mood=test_result.influence_by_active_mood
        )

    def to_base(self) -> 'TestResult':
        """to_base()

        Convert this into a TestResult.

        :return: A TestResult.
        :rtype: TestResult
        """
        return TestResult(
            self.result,
            self.reason,
            tooltip=self.tooltip,
            icon=self.icon,
            influence_by_active_mood=self.influence_by_active_mood
        )

    def __str__(self):
        if self.reason:
            return self.reason
        return str(self.result)

    def __repr__(self):
        if self.reason:
            return '<BBRunResult: {0} ({1})>'.format(repr(self.result), self.reason)
        return '<BBRunResult: {0}>'.format(repr(self.result))

    def __eq__(self, other):
        if isinstance(other, BBRunResult):
            return self.result == other.result
        return super().__eq__(other)

    def __bool__(self):
        if self.result:
            return True
        return False

    def __and__(self, other):
        result = self.result and other.result
        tooltip = self._tooltip_text or other._tooltip_text if hasattr(other, '_tooltip_text') else other.tooltip
        if self._reason:
            reason = self._reason
        else:
            reason = other._reason
        if result:
            icon = self.icon or other.icon
            influence_by_active_mood = self.influence_by_active_mood or other.influence_by_active_mood
        else:
            icon = None
            influence_by_active_mood = False
        return BBRunResult(result, reason, tooltip_text=tooltip, icon=icon, influence_by_active_mood=influence_by_active_mood)


BBRunResult.TRUE = BBRunResult(True, 'Success')
BBRunResult.FALSE = BBRunResult(False, 'Failure')
BBRunResult.NONE = BBRunResult(False, 'Failure')

