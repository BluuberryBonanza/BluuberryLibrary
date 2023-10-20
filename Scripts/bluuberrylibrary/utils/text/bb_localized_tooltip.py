"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union, Tuple, Any

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import TunableLocalizedStringFactory


# noinspection PyProtectedMember
class LocalizedTooltip(TunableLocalizedStringFactory._Wrapper):
    """LocalizedTooltip(string_id, tokens=())

    A class used when creating tooltips with localized strings.

    :param text: The text to display.
    :type text: int or str or LocalizedString
    :param tokens: The tokens to format into the text. Default is no tokens.
    :type tokens: Tuple[Any], optional
    """
    def __init__(self, text: Union[int, str, LocalizedString], tokens: Tuple[Any] = ()):
        super().__init__(text)
        self._tokens = tokens

    def __call__(self, *_) -> LocalizedString:
        from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils
        return BBLocalizationUtils.to_localized_string(self._string_id, tokens=self._tokens)
