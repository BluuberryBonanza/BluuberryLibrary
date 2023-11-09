"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.classes.bb_execute_interaction_result import BBExecuteInteractionResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult

# noinspection PyBroadException
try:
    from event_testing.results import TestResult, EnqueueResult
except:
    class EnqueueResult:
        def __init__(
            self,
            test_result: BBTestResult,
            execute_result: BBExecuteInteractionResult,
        ):
            self.test_result = test_result
            self.execute_result = execute_result


class BBEnqueueInteractionResult(EnqueueResult):
    """BBEnqueueInteractionResult(\
        test_result,\
        execute_result,\
    )

    The result of Enqueuing an interaction.

    :param test_result: The result of testing the interaction for Queue.
    :type test_result: BBTestResult
    :param execute_result: The result of executing the interaction.
    :type execute_result: BBExecuteInteractionResult
    """
    TRUE = None
    FALSE = None
    NONE = None

    def __init__(
        self,
        test_result: BBTestResult,
        execute_result: BBExecuteInteractionResult,
    ):
        pass

    @classmethod
    def from_base(cls, enqueue_result: EnqueueResult) -> 'BBEnqueueInteractionResult':
        """from_base(enqueue_result)

        Convert an EnqueueResult into a BBEnqueueInteractionResult.

        :param enqueue_result: The EnqueueResult to convert.
        :type enqueue_result: EnqueueResult
        :return: A BBEnqueueInteractionResult.
        :rtype: BBEnqueueInteractionResult
        """
        return BBEnqueueInteractionResult(
            enqueue_result.test_result,
            enqueue_result.execute_result
        )

    def to_base(self) -> 'EnqueueResult':
        """to_base()

        Convert this into a EnqueueResult.

        :return: A EnqueueResult.
        :rtype: EnqueueResult
        """
        return EnqueueResult(
            self.test_result,
            self.execute_result
        )

    def __str__(self):
        return '<BBEnqueueInteractionResult {0} - {1}>'.format(str(self.test_result), str(self.execute_result))

    def __repr__(self):
        return '<BBEnqueueInteractionResult {0} - {1}>'.format(repr(self.test_result), repr(self.execute_result))

    def __eq__(self, other):
        if isinstance(other, BBEnqueueInteractionResult):
            return self.test_result == other.test_result and self.execute_result == other.execute_result
        return super().__eq__(other)

    def __and__(self, other):
        test_result = self.test_result and other.test_result
        execute_result = self.execute_result and other.execute_result
        return BBEnqueueInteractionResult(test_result, execute_result)


BBEnqueueInteractionResult.TRUE = BBEnqueueInteractionResult(BBTestResult.TRUE, BBExecuteInteractionResult.NONE)
BBEnqueueInteractionResult.FALSE = BBEnqueueInteractionResult(BBTestResult.FALSE, BBExecuteInteractionResult.NONE)
BBEnqueueInteractionResult.NONE = BBEnqueueInteractionResult(BBTestResult.NONE, BBExecuteInteractionResult.NONE)

