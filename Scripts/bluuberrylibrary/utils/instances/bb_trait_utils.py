"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

import services
from sims4.resources import Types
from traits.traits import Trait


class BBTraitUtils:
    """Utilities for managing Traits."""
    @classmethod
    def load_trait_by_guid(cls, trait: int) -> Union[Trait, None]:
        """load_trait_by_guid(trait)

        Load a Trait by its GUID

        :param trait: The GUID of the Trait to load.
        :type trait: int
        :return: The loaded Trait or None if not found.
        :rtype: Trait or None
        """
        if isinstance(trait, Trait) or trait is Trait:
            return trait

        instance_manager = services.get_instance_manager(Types.TRAIT)
        return instance_manager.get(trait)
