"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.interactions.classes.bb_super_interaction import BBSuperInteraction
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim_info import SimInfo


class BBExampleSuperInteraction(BBSuperInteraction):
    # Both this Mod Identity function and the log name function are required to implement. You would implement using your own Mod Identity and a log name of your choosing.
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bb_example_super_interaction'

    # noinspection PyUnusedLocal
    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> TestResult:
        log = cls.get_log()
        if interaction_target is None or not isinstance(interaction_target, SimInfo):
            log.debug('Target is not a Sim.', interaction_target=interaction_target)
            return TestResult.NONE
        log.debug('Target is a Sim.', interaction_target=interaction_target)
        return TestResult.TRUE

    # noinspection PyUnusedLocal
    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo) -> TestResult:
        log = self.get_log()
        log.enable()
        log.debug('I ran the interaction!', target=interaction_target_sim_info)
        log.disable()
        return TestResult.TRUE

# In the Package file, you would have an Interaction Tuning that looks like this! Notice the "c" matches the Class name, and the "m" matches the Module path to this class.
# <?xml version="1.0" encoding="utf-8"?>
# <I c="BBExampleSuperInteraction" i="interaction" m="bluuberrylibrary.examples.bb_example_super_interaction" n="BBL_Example_Super_Interaction" s="15807679422315540817">
#   <V t="disabled" n="_saveable" />
#   <T n="cheat">True</T>
#   <T n="debug">True</T>
#   <T n="category">15787134577411302317<!--BBL_PieMenu_BluuberryLibrary--></T>
#   <T n="display_name">0x291AD434<!--Example Super Interaction--></T>
#   <L n="interaction_category_tags">
#     <E>Interaction_Super</E>
#     <E>Interaction_All</E>
#   </L>
#   <T n="pie_menu_priority">9</T>
#   <U n="progress_bar_enabled">
#     <T n="bar_enabled">False</T>
#   </U>
#   <E n="target_type">OBJECT</E>
# </I>
