"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

import services
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.household import Household
from sims.sim_info import SimInfo
from sims.sim_info_types import Gender, Age, SpeciesExtended
from sims.sim_spawner import SimSpawner, SimCreator
from sims.sim_spawner_enums import SimNameType


class BBSimSpawnUtils:
    """Utilities for spawning and despawning Sims."""

    @classmethod
    def spawn_sim(
        cls,
        sim_info: SimInfo,
        **kwargs
    ) -> bool:
        """spawn_sim(sim_info)

        Spawn a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if successful. False, if not.
        """
        if sim_info is None:
            return False
        if BBSimUtils.to_sim_instance(sim_info) is not None:
            return True
        active_sim_info = BBSimUtils.get_active_sim_info()
        active_sim = BBSimUtils.to_sim_instance(active_sim_info)
        location = active_sim.location
        position = location.transform.translation
        routing_surface = location.routing_surface
        if sim_info.is_baby:
            from sims.baby.baby_utils import create_and_place_baby
            create_and_place_baby(sim_info, position=location.transform, routing_surface=routing_surface)
        else:
            SimSpawner.spawn_sim(sim_info, sim_location=location, sim_position=position, **kwargs)
        return True

    @classmethod
    def create_sim_info(
        cls,
        species: SpeciesExtended,
        gender: Gender = Gender.MALE,
        age: Age = Age.ADULT,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        """create_sim_info(\
            species,\
            gender=None,\
            age=None,\
            source='testing'\
        )

        Create a new Sim.

        :param species: The species of the Sim.
        :type species: SpeciesExtended
        :param gender: The gender of the Sim. Default is MALE.
        :type gender: Gender, optional
        :param age: The age of the Sim. Default is ADULT.
        :type age: Age, optional
        :param source: The source of creation. Default is "testing".
        :type source: str, optional
        :return: The newly created Sim or None if an error occurs.
        :rtype: SimInfo or None
        """
        return cls._create_sim_info(
            species,
            gender=gender,
            age=age,
            source=source
        )

    @classmethod
    def _create_sim_info(
        cls,
        species: SpeciesExtended,
        gender: Gender = None,
        age: Age = None,
        breed_name: str = '',
        breed_name_key: int = 0,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        account = SimSpawner._get_default_account()
        household = Household(account, starting_funds=0)
        services.household_manager().add(household)
        if species is None or species == SpeciesExtended.INVALID:
            raise AssertionError(f'Invalid species specified for SimInfo creation! {species}')
        first_name = SimSpawner.get_random_first_name(gender, species=species, sim_name_type_override=SimNameType.DEFAULT)
        language = SimSpawner._get_language_for_locale(account.locale)
        family_name = SimSpawner._get_random_last_name(language, sim_name_type=SimNameType.DEFAULT)
        last_name = SimSpawner.get_last_name(family_name, gender, species=species)
        animal_species_list = (
            SpeciesExtended.DOG,
            SpeciesExtended.SMALLDOG,
            SpeciesExtended.FOX,
            SpeciesExtended.CAT,
            SpeciesExtended.HORSE
        )
        is_animal_species = False
        if species in animal_species_list:
            is_animal_species = True
        sim_creator = SimCreator(
            gender=gender,
            age=age,
            species=species,
            first_name=first_name,
            last_name=last_name,
            breed_name=breed_name if breed_name else 'Custom Breed' if is_animal_species else '',
            breed_name_key=breed_name_key if breed_name_key else 0x599432EA if is_animal_species else 0,
        )
        (sim_info_list, _) = SimSpawner.create_sim_infos((sim_creator,), household=household, generate_deterministic_sim=True, creation_source=source)
        if not sim_info_list:
            return None
        return sim_info_list[0]
