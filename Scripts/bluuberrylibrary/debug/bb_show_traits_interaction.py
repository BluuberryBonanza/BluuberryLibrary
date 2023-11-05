"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, List

from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_immediate_super_interaction import BBImmediateSuperInteraction
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.instances.bb_trait_utils import BBTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from distributor.shared_messages import IconInfoData
from interactions.context import InteractionContext
from sims.sim_info import SimInfo


class BBDebugShowTraitsInteraction(BBImmediateSuperInteraction):
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bb_show_traits_interaction'

    # noinspection PyUnusedLocal
    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        log = cls.get_log()
        if interaction_target is None or not isinstance(interaction_target, SimInfo):
            log.debug('Target is not correct.', interaction_target=interaction_target)
            return BBTestResult.NONE
        log.debug('Target is correct.', interaction_target=interaction_target)
        return BBTestResult.TRUE

    # noinspection PyUnusedLocal
    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo) -> BBRunResult:
        log = self.get_log()
        target_sim = BBSimUtils.to_sim_instance(interaction_target_sim_info)
        target_sim_info = BBSimUtils.to_sim_info(interaction_target_sim_info)
        trait_strings: List[str] = list()
        for trait in BBSimTraitUtils.get_traits(target_sim_info):
            trait_name = BBTraitUtils.get_trait_name(trait)
            trait_id = BBTraitUtils.get_trait_guid(trait)
            trait_strings.append('{} ({})'.format(trait_name, trait_id))

        trait_strings = sorted(trait_strings, key=lambda x: x)
        sim_traits = ', '.join(trait_strings)
        text = ''
        text += 'Traits:\n{}\n\n'.format(sim_traits)
        log.enable()
        sim_traits_for_log = ',\n'.join(trait_strings)
        for_log_text = 'Traits:\n{}\n\n'.format(sim_traits_for_log)
        log.debug(f'{target_sim_info} ({BBSimUtils.to_sim_id(target_sim_info)}): {for_log_text}')
        log.disable()
        from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
        BBNotification(
            f'{target_sim_info} Traits ({BBSimUtils.to_sim_id(target_sim_info)})',
            text
        ).show(
            icon=IconInfoData(obj_instance=target_sim)
        )
        return BBRunResult.TRUE
