"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple, Union

from bluuberrylibrary.dialogs.bb_dialog_response import BBDialogResponse
from bluuberrylibrary.enums.classes.bb_int import BBInt
from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils
from distributor.shared_messages import IconInfoData
from protocolbuffers.Localization_pb2 import LocalizedString
from ui.ui_dialog_notification import UiDialogNotification


class BBNotificationExpandBehavior(BBInt):
    USER_SETTING = UiDialogNotification.UiDialogNotificationExpandBehavior.USER_SETTING
    FORCE_EXPAND = UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND


class BBNotificationUrgency(BBInt):
    DEFAULT = UiDialogNotification.UiDialogNotificationUrgency.DEFAULT
    URGENT = UiDialogNotification.UiDialogNotificationUrgency.URGENT


class BBNotificationLevel(BBInt):
    PLAYER = UiDialogNotification.UiDialogNotificationLevel.PLAYER
    SIM = UiDialogNotification.UiDialogNotificationLevel.SIM


class BBNotificationVisualType(BBInt):
    INFORMATION = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
    SPEECH = UiDialogNotification.UiDialogNotificationVisualType.SPEECH
    SPECIAL_MOMENT = UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT


class BBNotificationAutoDeleteReason(BBInt):
    NO_REASON = UiDialogNotification.UiDialogNotificationAutoDeleteReason.NO_REASON
    LEAVE_LIVE_MODE = UiDialogNotification.UiDialogNotificationAutoDeleteReason.LEAVE_LIVE_MODE


class BBNotification:
    """A notification shown to the player.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        BBNotification(
            'I am a title',
            'I am a description'
        ).show()

    :param title: The title to show in the notification.
    :type title: int or str or LocalizedString
    :param description: The description to show in the notification.
    :type description: int or str or LocalizedString
    :param urgency: How urgent the notification will be. Default is Not Urgent. (Setting to URGENT will show orange box)
    :type urgency: BBNotificationUrgency, optional
    :param information_level: The level of information of the notification. Default is SIM.
    :type information_level: BBNotificationLevel, optional
    :param expand_behavior: How the notification should expand. Default is USER_SETTING.
    :type expand_behavior: BBNotificationExpandBehavior, optional
    :param visual_type: How the notification can appear to the player. Default is INFORMATION.
    :type visual_type: BBNotificationVisualType, optional
    :param auto_delete_reason: The reason for the notification to auto delete itself. Default is NO_REASON.
    :type auto_delete_reason: BBNotificationAutoDeleteReason, optional
    :param ui_responses: Responses used to create buttons in the notification and act on the results. Default is no buttons.
    :type ui_responses: Tuple[BBDialogReason], optional
    """
    def __init__(
        self,
        title: Union[int, str, LocalizedString],
        description: Union[int, str, LocalizedString],
        urgency: BBNotificationUrgency = BBNotificationUrgency.DEFAULT,
        information_level: BBNotificationLevel = BBNotificationLevel.SIM,
        expand_behavior: BBNotificationExpandBehavior = BBNotificationExpandBehavior.USER_SETTING,
        visual_type: BBNotificationVisualType = BBNotificationVisualType.INFORMATION,
        auto_delete_reason: BBNotificationAutoDeleteReason = BBNotificationAutoDeleteReason.NO_REASON,
        ui_responses: Tuple[BBDialogResponse] = ()
    ):
        self.title = BBLocalizationUtils.to_localized_string(title)
        self.description = BBLocalizationUtils.to_localized_string(description)
        self.visual_type = visual_type
        self.urgency = urgency
        self.information_level = information_level
        self.expand_behavior = expand_behavior
        self.auto_delete_reason = auto_delete_reason
        self.ui_responses = ui_responses

    def show(self, icon: IconInfoData = None, secondary_icon: IconInfoData = None):
        """show(icon=None, secondary_icon=None)

        Show the notification to the player.

        :param icon: The icon to show in the first icon slot. Default is no Icon.
        :type icon: IconInfoData, optional
        :param secondary_icon: The icon to show in the second icon slot. Default is no Icon.
        :type secondary_icon: IconInfoData, optional
        """
        _notification = self._create_notification()
        if _notification is None:
            return

        _notification.show_dialog(
            icon_override=icon,
            secondary_icon_override=secondary_icon
        )

    def _create_notification(self) -> UiDialogNotification:
        return UiDialogNotification.TunableFactory().default(
            None,
            title=lambda *args, **kwargs: self.title,
            text=lambda *args, **kwargs: self.description,
            visual_type=self.visual_type,
            urgency=self.urgency,
            information_level=self.information_level,
            ui_responses=self.ui_responses,
            expand_behavior=self.expand_behavior,
            auto_delete_reason=self.auto_delete_reason
        )