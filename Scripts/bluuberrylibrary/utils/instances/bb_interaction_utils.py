"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

import services
from interactions.base.interaction import Interaction
from sims4.resources import Types


class BBInteractionUtils:
    """Utilities for manipulating interactions."""

    @classmethod
    def to_interaction_guid(cls, interaction_identifier: Union[int, Interaction]) -> Union[int, None]:
        """to_interaction_guid(interaction_identifier)

        Convert an interaction identifier to a GUID.

        :param interaction_identifier: The identifier or instance of an Interaction.
        :type interaction_identifier: Union[int, Interaction]
        :return: The GUID of the Interaction or None, if the Interaction does not have a GUID.
        :rtype: Union[int, None]
        """
        if isinstance(interaction_identifier, int):
            return interaction_identifier
        return getattr(interaction_identifier, 'guid64', None)

    @classmethod
    def get_interaction_short_name(cls, interaction: Interaction) -> Union[str, None]:
        """get_interaction_short_name(interaction)

        Retrieve the Short Name of an Interaction.

        :param interaction: An instance of an interaction.
        :type interaction: Interaction
        :return: The short name of an interaction or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if interaction is None:
            return None
        # noinspection PyBroadException
        try:
            # noinspection PyUnresolvedReferences
            return str(interaction.shortname() or '') or interaction.__name__ or interaction.__class__.__name__
        except:
            # noinspection PyBroadException
            try:
                return interaction.__name__
            except:
                # noinspection PyBroadException
                try:
                    return interaction.__class__.__name__
                except:
                    return ''

    @classmethod
    def load_interaction_by_guid(cls, interaction: int) -> Union[Interaction, None]:
        """load_interaction_by_guid(interaction)

        Load an interaction by its GUID

        :param interaction: The GUID of the interaction to load.
        :type interaction: int
        :return: The loaded interaction or None if not found.
        :rtype: Interaction or None
        """
        if isinstance(interaction, Interaction):
            return interaction
        instance_manager = services.get_instance_manager(Types.INTERACTION)
        return instance_manager.get(interaction)
