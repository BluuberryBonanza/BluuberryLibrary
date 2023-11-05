"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.interactions.classes.bb_interaction_overrides_mixin import BBInteractionOverridesMixin
from bluuberrylibrary.logs.bb_log_mixin import BBLogMixin
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from event_testing.results import TestResult
from interactions.base.super_interaction import SuperInteraction
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from scheduling import Timeline
from sims.sim import Sim


class BBSuperInteraction(SuperInteraction, BBLogMixin, BBInteractionOverridesMixin):
    """An interaction that can either be a part of another interaction or be run on its own."""
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        raise NotImplementedError()

    @classmethod
    def get_log_name(cls) -> str:
        raise NotImplementedError()

    def __init__(self, *_, **__):
        super().__init__(*_, **__)
        BBLogMixin.__init__(self)
        BBInteractionOverridesMixin.__init__(self)

    @classmethod
    def _test(cls, target: Any, context: InteractionContext, **kwargs) -> TestResult:
        from event_testing.results import TestResult
        log = cls.get_log()
        try:
            sim_info = BBSimUtils.to_sim_info(context.sim)
            target_sim_info = target
            if target_sim_info is not None and isinstance(target_sim_info, Sim):
                target_sim_info = BBSimUtils.to_sim_info(target_sim_info)
            test_result = cls.bbl_test(sim_info, target_sim_info, context, **kwargs)
            if not test_result:
                return test_result.to_base()
        except Exception as ex:
            log.error(f'Error happened while running bbl_test of \'{cls.__name__}\'.', exception=ex)
            return TestResult(False, f'An error happened running bbl_test {ex}.')

        try:
            return super()._test(target, context, **kwargs)
        except Exception as ex:
            log.error(f'Error happened while running _test of \'{cls.__name__}\'.', exception=ex)
            return TestResult(False, f'An error happened running _test {ex}.')

    def _trigger_interaction_start_event(self: 'BBSuperInteraction'):
        log = self.get_log()
        try:
            sim_info = BBSimUtils.to_sim_info(self.sim)
            target = self.target
            if target is not None and isinstance(target, Sim):
                target = BBSimUtils.to_sim_info(self.target)
            result = self.bbl_started(sim_info, target)
            if result is not None and result.result:
                self.cancel(FinishingType.CONDITIONAL_EXIT, str(result))
                return
        except Exception as ex:
            log.error(f'Error happened when running bbl_started \'{self.__class__.__name__}\'.', exception=ex)

        try:
            return super()._trigger_interaction_start_event()
        except Exception as ex:
            log.error(f'Error happened while running _trigger_interaction_start_event of \'{self.__class__.__name__}\'.', exception=ex)

    def _run_interaction_gen(self, timeline: Timeline):
        log = self.get_log()
        try:
            sim_info = BBSimUtils.to_sim_info(self.sim)
            target = self.target
            if target is not None and isinstance(target, Sim):
                target = BBSimUtils.to_sim_info(self.target)
            result = self.bbl_run(sim_info, target, timeline)
            if not result:
                log.debug('Failed bbl_run', reason=result)
        except Exception as ex:
            log.error(f'Error happened when running bbl_run \'{self.__class__.__name__}\'.', exception=ex)

        try:
            yield from super()._run_interaction_gen(timeline)
        except Exception as ex:
            log.error(f'Error happened while running _run_interaction_gen of \'{self.__class__.__name__}\'.', exception=ex)
