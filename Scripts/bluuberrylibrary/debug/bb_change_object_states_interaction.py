"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple, Callable

from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.dialogs.bb_value_dialog import BBValueDialog
from bluuberrylibrary.dialogs.picker_rows.bb_value_picker_row import BBValuePickerRow
from bluuberrylibrary.enums.string_ids import BBStringId
from bluuberrylibrary.interactions.classes.bb_immediate_super_interaction import BBImmediateSuperInteraction
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.objects.bb_object_state_utils import BBObjectStateUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from interactions.context import InteractionContext
from objects.components.state import ObjectState, ObjectStateValue
from objects.game_object import GameObject
from sims.sim_info import SimInfo


class BBDebugChangeObjectStatesInteraction(BBImmediateSuperInteraction):
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bb_change_object_states_interaction'

    # noinspection PyUnusedLocal
    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target: GameObject, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        log = cls.get_log()
        if interaction_target is None:
            log.debug('Target is not correct.', interaction_target=interaction_target)
            return BBTestResult.NONE
        log.debug('Target is correct.', interaction_target=interaction_target)
        return BBTestResult.TRUE

    # noinspection PyUnusedLocal
    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target: GameObject) -> BBRunResult:
        log = self.get_log()
        self._open_change_object_states_dialog(interaction_target)
        return BBRunResult.TRUE

    def _open_change_object_states_dialog(self, game_object: GameObject):
        def _reopen():
            self._open_change_object_states_dialog(game_object)

        rows = list()
        object_states_and_values = BBObjectStateUtils.get_object_states_and_values(game_object)
        for (object_state, object_state_value) in object_states_and_values.items():
            rows.append(
                BBValuePickerRow(
                    len(rows),
                    object_state,
                    BBLocalizedStringData(f'{object_state} : {object_state_value}'),
                    BBLocalizedStringData(0)
                )
            )

        def _on_submit(chosen_values: Tuple[ObjectState]):
            chosen_state = next(iter(chosen_values), None)
            if chosen_state is None:
                return
            self._open_choose_object_state_value_dialog(game_object, chosen_state, _reopen)

        active_sim_info = BBSimUtils.get_active_sim_info()

        BBValueDialog(
            self.get_mod_identity(),
            BBLocalizedStringData(BBStringId.BBL_CHOOSE_OBJECT_STATES_TITLE),
            BBLocalizedStringData(BBStringId.BBL_CHOOSE_OBJECT_STATES_DESCRIPTION),
            tuple(rows),
        ).display(active_sim_info, _on_submit)

    def _open_choose_object_state_value_dialog(self, game_object: GameObject, object_state: ObjectState, on_close: Callable[[], None]):
        rows = list()
        current_object_state_value = BBObjectStateUtils.get_object_state_value(game_object, object_state)
        for object_state_value in object_state.values:
            rows.append(
                BBValuePickerRow(
                    len(rows),
                    object_state_value,
                    BBLocalizedStringData(f'{object_state_value}'),
                    BBLocalizedStringData(0),
                    is_selected=getattr(object_state_value, 'guid64') == getattr(current_object_state_value, 'guid64', None)
                )
            )

        def _on_submit(chosen_values: Tuple[ObjectStateValue]):
            self.get_log().debug('Got chosen value', chosen_values=chosen_values)
            chosen_state_value = next(iter(chosen_values), None)
            if chosen_state_value is None:
                on_close()
                return
            set_result = BBObjectStateUtils.apply_object_state_value(game_object, chosen_state_value)
            self.get_log().debug('Set result', set_result=set_result)
            on_close()

        active_sim_info = BBSimUtils.get_active_sim_info()

        BBValueDialog(
            self.get_mod_identity(),
            BBLocalizedStringData(BBStringId.BBL_CHOOSE_OBJECT_STATE_VALUE_TITLE),
            BBLocalizedStringData(BBStringId.BBL_CHOOSE_OBJECT_STATE_VALUE_DESCRIPTION, tokens=(str(object_state),)),
            tuple(rows),
        ).display(active_sim_info, _on_submit, on_closed=on_close)
