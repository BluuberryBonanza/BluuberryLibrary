"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union, Iterable, Any
from protocolbuffers.Localization_pb2 import LocalizedString


class BBLocalizedStringData:
    """BBLocalizedStringData(text, tokens=(), normalize_tokens=True)

    Data used when creating a localized string.

    :param text: The text to be displayed.
    :type text: int or str or LocalizedString
    :param tokens: Tokens to format into the text. Default is no tokens.
    :type tokens: Iterable[Any], optional
    :param normalize_tokens: If True, the tokens will be normalized into their own localized strings. Default is True.
    :type normalize_tokens: bool, optional
    """
    def __init__(
        self,
        text: Union[int, str, LocalizedString],
        tokens: Iterable[Any] = (),
        normalize_tokens: bool = True
    ):
        self.text = text
        self.tokens = tokens
        self.normalize_tokens = normalize_tokens

    def localize(self, additional_tokens: Iterable[Any] = ()) -> LocalizedString:
        """localize(additional_tokens=())

        Localize the display string into a Localized String.

        :param additional_tokens: Additional tokens to format into the text. Default is not tokens.
        :type additional_tokens: Iterable[Any], optional
        :return: A localized string.
        :rtype: LocalizedString
        """
        from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils
        return BBLocalizationUtils.to_localized_string(self.text, tokens=(*self.tokens, *additional_tokens), normalize_tokens=self.normalize_tokens)
