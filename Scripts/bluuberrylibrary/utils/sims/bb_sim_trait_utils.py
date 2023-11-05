"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union, List

import services
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.utils.instances.bb_trait_utils import BBTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo
from traits.trait_tracker import TraitTracker
from traits.trait_type import TraitType
from traits.traits import Trait


class BBSimTraitUtils:
    """Utilities for managing Traits on Sims."""
    @classmethod
    def has_trait(cls, sim_info: SimInfo, trait: Union[int, Trait]) -> bool:
        """has_trait(sim_info, trait)

        Check if a Sim has a trait or not.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param trait: The trait to check for.
        :type trait: int or Trait
        :return: True, if the Sim has the trait. False, if not.
        :rtype: bool
        """
        trait_instance = BBTraitUtils.load_trait_by_guid(trait)
        if trait_instance is None:
            return False
        return sim_info.has_trait(trait_instance)

    @classmethod
    def add_trait(cls, sim_info: SimInfo, trait: Union[int, Trait]) -> BBRunResult:
        """add_trait(sim_info, trait)

        Add a Trait to a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param trait: The Trait to add.
        :type trait: int or Trait
        :return: The result of adding or failing to add the trait. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        if sim_info is None:
            raise AssertionError('Cannot add a trait to a None Sim.')
        trait_instance = BBTraitUtils.load_trait_by_guid(trait)
        if trait_instance is None:
            return BBRunResult(False, f'No trait existed with GUID {trait}.')
        can_add_result = cls.can_add_trait(sim_info, trait)
        if not can_add_result:
            return can_add_result
        added = sim_info.add_trait(trait_instance)
        if added is None:
            return BBRunResult(False, f'Failed to add trait {trait_instance} to Sim {sim_info}.')
        return BBRunResult(True, f'Successfully added trait {trait_instance} to Sim {sim_info}.')

    @classmethod
    def get_traits(cls, sim_info: SimInfo) -> List[Trait]:
        """get_traits(sim_info)

        Get traits on a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: A list of Traits.
        :rtype: List[Trait]
        """
        if isinstance(sim_info, SimInfo):
            if not hasattr(sim_info, 'get_traits'):
                return list()
            traits = list(sim_info.get_traits())
            if traits:
                return traits
            if not hasattr(sim_info, '_base'):
                return traits
            return list([BBTraitUtils.load_trait_by_guid(trait_id) for trait_id in (*sim_info._base.trait_ids, *sim_info._base.base_trait_ids) if BBTraitUtils.load_trait_by_guid(trait_id) is not None])
        return list()

    @classmethod
    def can_add_trait(cls, sim_info: SimInfo, trait: Union[int, Trait]) -> BBRunResult:
        """can_add_trait(sim_info, trait)

        Determine if a Trait can be added to the Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param trait: The Trait to check.
        :type trait: int or Trait
        :return: True, if the Trait can be added to the Sim. False, if not.
        :rtype: BBRunResult
        """
        if sim_info is None:
            raise AssertionError('Cannot add a trait to a None Sim.')
        trait_instance = BBTraitUtils.load_trait_by_guid(trait)
        if trait_instance is None:
            return BBRunResult(False, f'Cannot add trait to Sim {sim_info}. No trait existed with GUID {trait}.')
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return BBRunResult(False, f'Cannot add trait {trait_instance} to Sim {sim_info} because they are not currently spawned.')
        trait_tracker: TraitTracker = sim_info._trait_tracker
        if not trait_tracker._has_valid_lod(trait_instance):
            return BBRunResult(False, f'Trying to equip a trait {trait_instance} for Sim {sim_info} without meeting the min lod (sim: {sim_info.lod} < trait: {trait_instance.min_lod_value})')
        if trait_tracker.has_trait(trait_instance):
            return BBRunResult(False, f'Trying to equip an existing trait {trait_instance} for Sim {sim_info}')
        if trait_instance.is_personality_trait and trait_tracker.available_personality_trait_count == 0:
            return BBRunResult(False, f'Reach max trait number {trait_tracker.available_personality_trait_count} for Sim {sim_info}')
        if trait_instance.is_preference_trait and trait_tracker.at_preference_capacity():
            return BBRunResult(False, f'Reached max preference-traits for Sim {sim_info}')
        if not trait_instance.is_valid_trait(sim_info):
            return BBRunResult(False, f"Trying to equip a trait {trait_instance} that conflicts with Sim {sim_info}'s age {sim_info.age} or gender {sim_info.gender}")
        if trait_tracker.is_conflicting(trait_instance):
            return BBRunResult(False, f'Trying to equip a conflicting trait {trait_instance} for Sim {sim_info}')
        if trait_instance.trait_type == TraitType.LIFESTYLE and not services.lifestyle_service().lifestyles_enabled:
            return BBRunResult(False, f'Trying to equip a lifestyle trait {trait_instance} for Sim {sim_info} without lifestyles enabled')
        import mtx
        if trait_instance.entitlement is not None and not mtx.has_entitlement(trait_instance.entitlement):
            return BBRunResult(False, f'Trying to equip a trait {trait_instance} for Sim {sim_info} without proper entitlement')
        elif trait_tracker._is_excluded(trait_instance):
            return BBRunResult(False, f'Trying to equip a trait {trait_instance} for Sim {sim_info} which is excluded by a different trait.')
        return BBRunResult(True, f'Can add {trait_instance} to Sim {sim_info}.')

    @classmethod
    def remove_trait(cls, sim_info: SimInfo, trait: Union[int, Trait]) -> BBRunResult:
        """remove_trait(sim_info, trait)

        Remove a trait from a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param trait: The Trait to remove.
        :type trait: int or Trait
        :return: True, if the Trait was successfully removed. False, if not.
        :rtype: BBRunResult
        """
        if sim_info is None:
            raise AssertionError('Cannot remove a trait from a None Sim.')
        trait_instance = BBTraitUtils.load_trait_by_guid(trait)
        if trait_instance is None:
            return BBRunResult(False, f'Cannot remove trait from Sim {sim_info}. No trait existed with GUID {trait}.')
        result = sim_info.remove_trait(trait_instance)
        if result:
            return BBRunResult(True, f'Successfully removed Trait {trait_instance} from Sim {sim_info}.')
        return BBRunResult(False, f'Failed to remove Trait {trait_instance} from Sim {sim_info}.')
