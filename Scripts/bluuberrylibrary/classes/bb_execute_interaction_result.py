"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from interactions.base.interaction import Interaction

# noinspection PyBroadException
try:
    from event_testing.results import TestResult, EnqueueResult, ExecuteResult
except:
    class ExecuteResult:
        def __init__(
            self,
            result: bool,
            interaction: Union[Interaction, None],
            reason: str
        ):
            self.result = result
            self.interaction = interaction
            self.reason = reason


class BBExecuteInteractionResult(ExecuteResult):
    """BBExecuteInteractionResult(\
        result,\
        interaction,\
        reason,\
    )

    The result of executing an interaction.

    :param result: Set to True, if execution was successful. Set to False, if not.
    :type result: bool
    :param interaction: The interaction that was executed.
    :type interaction: Interaction
    :param reason: The reason for a failure or success.
    :type reason: str
    """
    NONE = None

    def __init__(
        self,
        result: bool,
        interaction: Union[Interaction, None],
        reason: str,
    ):
        pass

    @classmethod
    def from_base(cls, execute_result: ExecuteResult) -> 'BBExecuteInteractionResult':
        """from_base(execute_result)

        Convert an ExecuteResult into a BBExecuteInteractionResult.

        :param execute_result: The ExecuteResult to convert.
        :type execute_result: ExecuteResult
        :return: A BBExecuteInteractionResult.
        :rtype: BBExecuteInteractionResult
        """
        return BBExecuteInteractionResult(
            execute_result.result,
            execute_result.interaction,
            execute_result.reason
        )

    def to_base(self) -> 'ExecuteResult':
        """to_base()

        Convert this into a ExecuteResult.

        :return: A ExecuteResult.
        :rtype: ExecuteResult
        """
        return ExecuteResult(
            self.result,
            self.interaction,
            self.reason
        )

    def __str__(self):
        if self.reason:
            return self.reason
        return str(self.result)

    def __repr__(self):
        if self.interaction is not None:
            if self.reason:
                return f'<BBExecuteInteractionResult: {self.result}: ({self.reason}) - {self.interaction}>'
            else:
                return f'<BBExecuteInteractionResult: {self.result} - {self.interaction}>'
        if self.reason:
            return f'<BBExecuteInteractionResult: {self.result}: ({self.reason})>'
        return f'<BBExecuteInteractionResult: {self.result}>'

    def __eq__(self, other):
        if isinstance(other, BBExecuteInteractionResult):
            return self.result == other.result
        return super().__eq__(other)

    def __bool__(self):
        if self.result:
            return True
        return False

    def __and__(self, other):
        result = self.result and other.result
        if self.reason:
            reason = self.reason
        else:
            reason = other.reason
        if self.interaction is not None:
            interaction = self.interaction
        else:
            interaction = other.interaction
        return BBExecuteInteractionResult(result, interaction, reason, )


BBExecuteInteractionResult.NONE = BBExecuteInteractionResult(False, None, 'Failure')

