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
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from interactions.social.social_super_interaction import SocialSuperInteraction
from sims.sim import Sim
from sims4.utils import flexmethod


class BBSocialSuperInteraction(SocialSuperInteraction, BBLogMixin, BBInteractionOverridesMixin):
    """An interaction that occurs when a Sim is interacting with another Sim."""
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

    # noinspection PyMethodParameters
    @flexmethod
    def _test(cls, inst: 'BBSocialSuperInteraction', target: Any, context: InteractionContext, **kwargs) -> TestResult:
        inst_or_cls = inst or cls
        log = inst_or_cls.get_log()
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
            super_result = super(BBSocialSuperInteraction, inst_or_cls)._test(target, context, **kwargs)
            if not super_result:
                log.debug('Super Result', super_result=super_result)
            return super_result
        except Exception as ex:
            log.error(f'Error happened while running _test of \'{cls.__name__}\'.', exception=ex)
            return TestResult(False, f'An error happened running _test {ex}.')

    def _trigger_interaction_start_event(self: 'BBSocialSuperInteraction'):
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

    def cancel(self, finishing_type, cancel_reason_msg, **kwargs):
        log = self.get_log()
        try:
            sim_info = BBSimUtils.to_sim_info(self.sim)
            target = self.target
            if target is not None and isinstance(target, Sim):
                target = BBSimUtils.to_sim_info(self.target)
            self.bbl_cancelled(sim_info, target, self.context, finishing_type, cancel_reason_msg, **kwargs)
        except Exception as ex:
            log.error(f'Error happened when running bbl_cancelled \'{self.__class__.__name__}\'.', exception=ex)

        try:
            return super().cancel(finishing_type, cancel_reason_msg, **kwargs)
        except Exception as ex:
            log.error(f'Error happened while running cancel of \'{self.__class__.__name__}\'.', exception=ex)
