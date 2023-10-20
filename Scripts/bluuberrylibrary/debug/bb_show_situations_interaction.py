"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_immediate_super_interaction import BBImmediateSuperInteraction
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.instances.bb_situation_utils import BBSituationUtils
from bluuberrylibrary.utils.sims.bb_sim_situation_utils import BBSimSituationUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions.context import InteractionContext
from sims.sim_info import SimInfo


class BBDebugShowSituationsInteraction(BBImmediateSuperInteraction):
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bb_show_situations_interaction'

    # noinspection PyUnusedLocal
    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        """bbl_test(interaction_sim_info, interaction_target, interaction_context, *args, **kwargs)

        Occurs when testing the interaction.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: BBTestResult
        """
        log = cls.get_log()
        if interaction_target is None or not isinstance(interaction_target, SimInfo):
            log.debug('Target is not correct.', interaction_target=interaction_target)
            return BBTestResult.NONE
        log.debug('Target is correct.', interaction_target=interaction_target)
        return BBTestResult.TRUE

    # noinspection PyUnusedLocal
    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo) -> BBTestResult:
        """bbl_started(interaction_sim_info, interaction_target)

        Occurs when starting the interaction.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target_sim_info: The target Object of the interaction.
        :type interaction_target_sim_info: Any
        :return: The result of running the start function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: BBTestResult
        """
        log = self.get_log()
        target_sim_instance = BBSimUtils.to_sim_instance(interaction_target_sim_info)
        situation_texts = list()
        for situation in BBSimSituationUtils.get_situations(interaction_target_sim_info):
            situation_name = BBSituationUtils.get_situation_name(situation)
            situation_id = BBSituationUtils.get_situation_guid(situation)
            situation_job = BBSimSituationUtils.get_situation_job(interaction_target_sim_info, situation)
            job_name = BBSituationUtils.get_situation_job_name(situation_job)

            situation_role = BBSimSituationUtils.get_situation_role(interaction_target_sim_info, situation)
            role_name = BBSituationUtils.get_situation_role_name(situation_role)
            situation_texts.append(f'Situation: {situation_name} ({situation_id}). Role: {role_name} Job {situation_job}')

        situation_texts = sorted(situation_texts, key=lambda x: x)

        log.enable()
        sim_id = BBSimUtils.to_sim_id(interaction_target_sim_info)
        log.debug(f'{interaction_target_sim_info} ({sim_id}) Situations')
        if not situation_texts:
            log.debug('No Situations.')
        else:
            text = '\n\n'.join(situation_texts)
            log.debug(text)
        log.disable()
        return BBTestResult.TRUE
