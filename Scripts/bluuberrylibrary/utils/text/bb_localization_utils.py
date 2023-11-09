"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, Union, Iterable

from bluuberrylibrary.enums.string_ids import BBStringId
from bluuberrylibrary.utils.text.bb_localized_tooltip import BBLocalizedTooltip
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import TunableLocalizedStringFactory


class BBLocalizationUtils:
    """Utilities for manipulating Localized Strings."""

    @classmethod
    def to_localized_tooltip(cls, text: Union[int, str], tokens: Iterable[Any] = (), normalize_tokens: bool = True) -> BBLocalizedTooltip:
        """to_localized_tooltip(text, tokens=(), normalize_tokens=True)

        Convert an Integer or String into a Localized Tooltip.

        :param text: The text or string ID to convert.
        :type text: int or str
        :param tokens: Tokens to format into the text. Default is no tokens.
        :type tokens: Tuple[Any], optional
        :param normalize_tokens: If True, the tokens will be normalized into their own localized strings. Default is True.
        :type normalize_tokens: bool, optional
        :return: A localized tooltip.
        :rtype: BBLocalizedTooltip
        """
        if text is None:
            raise AssertionError('Missing String!')
        from bluuberrylibrary.utils.text.bb_localized_tooltip_data import BBLocalizedTooltipData
        if isinstance(text, BBLocalizedTooltipData):
            return text.localize(additional_tokens=tokens)
        return BBLocalizedTooltip(text, tokens=tokens, normalize_tokens=normalize_tokens)

    @classmethod
    def to_localized_string(
        cls,
        text: Union[int, str, LocalizedString],
        tokens: Iterable[Any] = (),
        normalize_tokens: bool = True
    ) -> LocalizedString:
        """to_localized_string(text, tokens=(), normalize_tokens=True)

        Convert an Integer or String into a Localized String.

        :param text: The text or string ID to convert.
        :type text: int or str
        :param tokens: Tokens to format into the text. Default is no tokens.
        :type tokens: Tuple[Any], optional
        :param normalize_tokens: If True, the tokens will be normalized into their own localized strings. Default is True.
        :type normalize_tokens: bool, optional
        :return: A localized string.
        :rtype: LocalizedString
        """
        if text is None:
            raise AssertionError('Missing String!')

        if normalize_tokens:
            if tokens:
                tokens = tuple(cls._normalize_tokens(tokens))
        if isinstance(text, LocalizedString) and hasattr(text, 'tokens'):
            from sims4.localization import create_tokens
            create_tokens(text.tokens, tokens)
            return text
        from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
        if isinstance(text, BBLocalizedStringData):
            return text.localize(additional_tokens=tokens)
        # noinspection PyProtectedMember
        if isinstance(text, TunableLocalizedStringFactory._Wrapper):
            # noinspection PyProtectedMember
            if isinstance(text._string_id, str):
                # noinspection PyProtectedMember
                localized_string = cls._localized_string_from_string(text._string_id)
            else:
                # noinspection PyProtectedMember
                localized_string = cls._localized_string_from_int(text._string_id, *tuple(tokens))
            return localized_string
        if isinstance(text, int):
            return cls._localized_string_from_int(text, tokens=tokens)
        if hasattr(text, 'sim_info'):
            return text.sim_info
        if hasattr(text, 'get_sim_info'):
            return text.get_sim_info()
        if isinstance(text, str):
            return cls._localized_string_from_string(text)
        return cls._localized_string_from_string(str(text))

    @classmethod
    def _normalize_tokens(cls, tokens: Iterable[Any]) -> Iterable[LocalizedString]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(cls.to_localized_string(token))
        return tuple(new_tokens)

    @classmethod
    def combine_strings(cls, text_list: Iterable[Union[int, str, LocalizedString]], separator_text: int = BBStringId.BBL_STRING_COMMA_STRING) -> LocalizedString:
        """combine_strings(text_list, separator_text=BBStringId.BBL_STRING_COMMA_STRING)

        Combine multiple strings by a separation string.

        :param text_list: The text to combine.
        :type text_list: Iterable[int or str or LocalizedString]
        :param separator_text: The text that will act as the separator.
        :type separator_text: int
        :return: A combined string.
        :rtype: LocalizedString
        """
        localized = None
        for text in text_list:
            if localized is None:
                localized = text
            else:
                localized = cls.to_localized_string(separator_text, tokens=(localized, text))
        return localized

    @classmethod
    def _localized_string_from_string(cls, text: str) -> LocalizedString:
        from sims4.localization import LocalizationHelperTuning
        return LocalizationHelperTuning.get_raw_text(text)

    @classmethod
    def _localized_string_from_int(cls, identifier: int, tokens: Iterable[Any] = ()) -> LocalizedString:
        # noinspection PyProtectedMember
        from sims4.localization import _create_localized_string
        return _create_localized_string(identifier, *tokens)
