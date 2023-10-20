"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union, List

from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils
from interactions.utils.loot import LootActions
from interactions.utils.tunable_icon import TunableIcon
from ui.ui_dialog import UiDialogResponse, ButtonType, _UiResponseCommand, UiResponseParticipantId


class BBUIResponseCommand(_UiResponseCommand):
    def __init__(
        self,
        command: str,
        arguments: List[Union[bool, str, float, int, UiResponseParticipantId]]
    ):
        super().__init__(command, arguments)


class BBDialogResponse(UiDialogResponse):

    def __init__(
        self,
        text: Union[int, str],
        subtext: Union[int, str] = None,
        button_icon: TunableIcon = None,
        disabled_text: Union[int, str] = None,
        tooltip_text: Union[int, str] = None,
        sort_order: int = 0,
        dialog_response_id: int = ButtonType.DIALOG_RESPONSE_NO_RESPONSE,
        ui_request: UiDialogResponse.UiDialogUiRequest = UiDialogResponse.UiDialogUiRequest.NO_REQUEST,
        response_command: BBUIResponseCommand = None,
        audio_event_name: str = None,
        tutorial_id: int = None,
        loots_for_response: List[LootActions] = None,
        ui_message_name: str = None
    ):
        if text is not None:
            text = BBLocalizationUtils.to_localized_string(text)
        if subtext is not None:
            subtext = BBLocalizationUtils.to_localized_string(subtext)
        if disabled_text is not None:
            disabled_text = BBLocalizationUtils.to_localized_string(disabled_text)
        if tooltip_text is not None:
            tooltip_text = BBLocalizationUtils.to_localized_tooltip(tooltip_text)
        super().__init__(
            sort_order=sort_order,
            dialog_response_id=dialog_response_id,
            text=text,
            subtext=subtext,
            ui_request=ui_request,
            response_command=response_command,
            disabled_text=disabled_text,
            audio_event_name=audio_event_name,
            tutorial_id=tutorial_id,
            tooltip_text=tooltip_text,
            button_icon=button_icon,
            loots_for_response=loots_for_response,
            ui_message_name=ui_message_name
        )
