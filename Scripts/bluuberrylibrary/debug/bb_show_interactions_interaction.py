"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, List

from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.dialogs.icons.bb_sim_icon_info import BBSimIconInfo
from bluuberrylibrary.interactions.classes.bb_immediate_super_interaction import BBImmediateSuperInteraction
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from bluuberrylibrary.utils.sims.bb_sim_interaction_utils import BBSimInteractionUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from interactions.context import InteractionContext
from sims.sim_info import SimInfo


class BBDebugShowInteractionsInteraction(BBImmediateSuperInteraction):
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bb_show_interactions_interaction'

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
    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo) -> BBRunResult:
        """bbl_started(interaction_sim_info, interaction_target)

        Occurs when starting the interaction.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target_sim_info: The target Object of the interaction.
        :type interaction_target_sim_info: Any
        :return: The result of running the start function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: BBRunResult
        """
        log = self.get_log()
        running_interaction_strings: List[str] = list()
        for interaction in BBSimInteractionUtils.get_running_interactions_gen(interaction_target_sim_info):
            interaction_name = BBInteractionUtils.get_interaction_short_name(interaction)
            interaction_id = BBInteractionUtils.to_interaction_guid(interaction)
            running_interaction_strings.append(f'{interaction_name} ({interaction_id})')
        running_interaction_strings = sorted(running_interaction_strings, key=lambda x: x)
        running_interaction_names = ', '.join(running_interaction_strings)

        queued_interaction_strings: List[str] = list()
        for interaction in BBSimInteractionUtils.get_queued_interactions_gen(interaction_target_sim_info):
            interaction_name = BBInteractionUtils.get_interaction_short_name(interaction)
            interaction_id = BBInteractionUtils.to_interaction_guid(interaction)
            queued_interaction_strings.append(f'{interaction_name} ({interaction_id})')
        queued_interaction_strings = sorted(queued_interaction_strings, key=lambda x: x)
        queued_interaction_names = ', '.join(queued_interaction_strings)
        text = ''
        text += f'Running:\n{running_interaction_names}\n\n'
        text += f'Queued:\n{queued_interaction_names}\n\n'
        log.enable()
        sim_running_interactions_for_log = ',\n'.join(running_interaction_strings)
        for_log_text = f'Running:\n{sim_running_interactions_for_log}\n\n'
        sim_queued_interactions_for_log = ',\n'.join(queued_interaction_strings)
        for_log_text += f'Queued:\n{sim_queued_interactions_for_log}\n\n'
        log.debug(f'{interaction_target_sim_info} ({BBSimUtils.to_sim_id(interaction_target_sim_info)}): {for_log_text}')
        log.disable()
        from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
        BBNotification(
            self.get_mod_identity(),
            BBLocalizedStringData('Interactions Of Sim'),
            BBLocalizedStringData(for_log_text)
        ).show(icon=BBSimIconInfo(interaction_target_sim_info))
        return BBRunResult.TRUE
