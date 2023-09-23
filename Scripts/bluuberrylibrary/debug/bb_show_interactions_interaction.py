"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, List, TYPE_CHECKING

from bluuberrylibrary.logs.bb_log import BBLog
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from bluuberrylibrary.utils.sims.bb_sim_interaction_utils import BBSimInteractionUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from event_testing.results import TestResult
from event_testing.tests import TestList
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from sims.sim import Sim
from sims.sim_info import SimInfo

if TYPE_CHECKING:
    from interactions.base.interaction import Interaction


class BBDebugShowInteractionsInteraction(ImmediateSuperInteraction):
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log(cls) -> BBLog:
        return BBLogRegistry().register_log(cls.get_mod_identity(), 'bb_show_interactions_interaction')

    # noinspection PyUnusedLocal
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> TestResult:
        """on_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs upon the interaction being tested for availability.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: TestResult
        """
        log = cls.get_log()
        if interaction_target is None or (not isinstance(interaction_target, Sim) and not isinstance(interaction_target, SimInfo)):
            log.debug('Target is not correct.', interaction_target=interaction_target)
            return TestResult.NONE
        log.debug('Target is correct.', interaction_target=interaction_target)
        return TestResult.TRUE

    # noinspection PyUnusedLocal
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> TestResult:
        """on_started(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being started.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: The result of running the start function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: TestResult
        """
        log = self.get_log()
        target_sim_info = BBSimUtils.to_sim_info(interaction_target)
        target_sim_instance = BBSimUtils.to_sim_instance(target_sim_info)
        running_interaction_strings: List[str] = list()
        for interaction in BBSimInteractionUtils.get_running_interactions_gen(target_sim_info):
            interaction_name = BBInteractionUtils.get_interaction_short_name(interaction)
            interaction_id = BBInteractionUtils.to_interaction_guid(interaction)
            running_interaction_strings.append(f'{interaction_name} ({interaction_id})')
        running_interaction_strings = sorted(running_interaction_strings, key=lambda x: x)
        running_interaction_names = ', '.join(running_interaction_strings)

        queued_interaction_strings: List[str] = list()
        for interaction in BBSimInteractionUtils.get_queued_interactions_gen(target_sim_info):
            interaction_name = BBInteractionUtils.get_interaction_short_name(interaction)
            interaction_id = BBInteractionUtils.to_interaction_guid(interaction)
            queued_interaction_strings.append(f'{interaction_name} ({interaction_id})')
        queued_interaction_strings = sorted(queued_interaction_strings, key=lambda x: x)
        queued_interaction_names = ', '.join(queued_interaction_strings)
        text = ''
        text += f'Running Interactions:\n{running_interaction_names}\n\n'
        text += f'Queued Interactions:\n{queued_interaction_names}\n\n'
        log.enable()
        sim_running_interactions_for_log = ',\n'.join(running_interaction_strings)
        for_log_text = f'Running Interactions:\n{sim_running_interactions_for_log}\n\n'
        sim_queued_interactions_for_log = ',\n'.join(queued_interaction_strings)
        for_log_text += f'Queued Interactions:\n{sim_queued_interactions_for_log}\n\n'
        log.debug(f'{target_sim_instance} ({BBSimUtils.to_sim_id(target_sim_info)}): {for_log_text}')
        log.disable()
        return TestResult.TRUE

    # noinspection PyUnusedLocal
    @classmethod
    def on_post_super_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> TestResult:
        """on_post_super_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs after the interaction being tested for availability by on_test and the super _test functions.

        .. note:: This will only run if both on_test and _test returns TestResult.TRUE or similar.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: TestResult
        """
        return TestResult.TRUE

    @classmethod
    def _test(cls, target: Any, context: InteractionContext, super_interaction: 'Interaction'=None, skip_safe_tests: bool=False, **kwargs) -> TestResult:
        from event_testing.results import TestResult
        log = cls.get_log()
        try:
            try:
                log.debug(
                    'Running on_test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    super_interaction=super_interaction,
                    skip_safe_tests=skip_safe_tests,
                    kwargles=kwargs
                )
                test_result = cls.on_test(context.sim, target, context, super_interaction=super_interaction, skip_safe_tests=skip_safe_tests, **kwargs)
                log.debug('Test Result (ImmediateSuperInteraction)', test_result=test_result)
            except Exception as ex:
                log.error('Error occurred while running ImmediateSuperInteraction \'{}\' on_test.'.format(cls.__name__), exception=ex)
                return TestResult(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/bb_logs/<mod_name>_Exceptions.txt"')

            if test_result is not None:
                if isinstance(test_result, TestResult) and test_result.result is False:
                    tooltip = None
                    return TestResult(test_result.result, test_result.reason, tooltip=tooltip, icon=test_result.icon, influence_by_active_mood=test_result.influence_by_active_mood)

            try:
                log.debug(
                    'Running super()._test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    super_interaction=super_interaction,
                    skip_safe_tests=skip_safe_tests,
                    kwargles=kwargs
                )
                super_test_result: TestResult = super()._test(target, context, super_interaction=super_interaction, skip_safe_tests=skip_safe_tests, **kwargs)
                if log.is_enabled():
                    search_for_tooltip = context.source == context.SOURCE_PIE_MENU
                    resolver = cls.get_resolver(target=target, context=context, super_interaction=super_interaction, search_for_tooltip=search_for_tooltip, **kwargs)
                    global_result = cls.test_globals.run_tests(resolver, skip_safe_tests, search_for_tooltip=search_for_tooltip)
                    local_result = cls.tests.run_tests(resolver, skip_safe_tests=skip_safe_tests, search_for_tooltip=search_for_tooltip)
                    if cls._additional_tests:
                        additional_tests = TestList(cls._additional_tests)
                        additional_local_result = additional_tests.run_tests(resolver, skip_safe_tests=skip_safe_tests, search_for_tooltip=search_for_tooltip)
                    else:
                        additional_local_result = None
                    if cls.test_autonomous:
                        autonomous_result = cls.test_autonomous.run_tests(resolver, skip_safe_tests=skip_safe_tests, search_for_tooltip=False)
                    else:
                        autonomous_result = None
                    if target is not None:
                        tests = target.get_affordance_tests(cls)
                        if tests is not None:
                            target_result = tests.run_tests(resolver, skip_safe_tests=skip_safe_tests, search_for_tooltip=search_for_tooltip)
                        else:
                            target_result = None
                    else:
                        target_result = None
                    log.debug('Super Test Result (ImmediateSuperInteraction)', super_test_result=super_test_result, global_result=global_result, local_result=local_result, additional_local_result=additional_local_result, autonomous_result=autonomous_result, target_result=target_result)
            except Exception as ex:
                log.error('Error occurred while running ImmediateSuperInteraction \'{}\' super()._test.'.format(cls.__name__), exception=ex)
                return TestResult(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/bb_logs/<mod_name>_Exceptions.txt"')

            if super_test_result is not None and isinstance(test_result, TestResult) and not super_test_result.result:
                return test_result

            try:
                log.debug(
                    'Running on_post_super_test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    super_interaction=super_interaction,
                    skip_safe_tests=skip_safe_tests,
                    kwargles=kwargs
                )
                post_super_test_result = cls.on_post_super_test(context.sim, target, context, super_interaction=super_interaction, skip_safe_tests=skip_safe_tests, **kwargs)
                log.debug('Post Test Result (ImmediateSuperInteraction)', post_super_test_result=post_super_test_result)
            except Exception as ex:
                log.error('Error occurred while running ImmediateSuperInteraction \'{}\' on_post_super_test.'.format(cls.__name__), exception=ex)
                return TestResult(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/bb_logs/<mod_name>_Exceptions.txt"')

            if post_super_test_result is not None:
                if isinstance(post_super_test_result, TestResult) and post_super_test_result.result is False:
                    post_super_test_result_tooltip = None
                    return TestResult(post_super_test_result.result, post_super_test_result.reason, tooltip=post_super_test_result_tooltip, icon=post_super_test_result.icon, influence_by_active_mood=post_super_test_result.influence_by_active_mood)

            return TestResult(True)
        except Exception as ex:
            log.error('Error occurred while running _test of ImmediateSuperInteraction \'{}\''.format(cls.__name__), exception=ex)
            return TestResult(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/bb_logs/<mod_name>_Exceptions.txt"')

    def _trigger_interaction_start_event(self: 'BBDebugShowInteractionsInteraction'):
        log = self.get_log()
        try:
            log.debug(
                'Running on_started.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            result = self.on_started(self.sim, self.target)
            if result is not None and result.result:
                self.cancel(FinishingType.CONDITIONAL_EXIT, str(result))
                return False
            return super()._trigger_interaction_start_event()
        except Exception as ex:
            log.error(f'Error happened when running \'{self.__class__.__name__}\' on_started.', exception=ex)
