"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Iterator, Union

import services
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from role.role_state import RoleState
from sims.sim_info import SimInfo
from situations.situation import Situation
from situations.situation_job import SituationJob


class BBSimSituationUtils:
    """Utilities for manipulating the situations of Sims."""
    @classmethod
    def get_situations(cls, sim_info: SimInfo) -> Iterator[Situation]:
        """get_situations(sim_info)

        Get all situations a Sim is in.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterator of Situations.
        :rtype: Iterator[Situation]
        """
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return
        for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim):
            yield situation

    @classmethod
    def get_situation_job(cls, sim_info: SimInfo, situation: Situation) -> Union[SituationJob, None]:
        """get_situation_job(sim_info, situation)

        Get the current Situation Job a Sim is assigned to in a Situation.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param situation: A situation.
        :type situation: Situation
        :return: The Situation Job the Sim is assigned to in the Situation or None if the Sim is not running the Situation.
        :rtype: SituationJob or None
        """
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return None
        return situation.get_current_job_for_sim(sim)

    @classmethod
    def get_situation_role(cls, sim_info: SimInfo, situation: Situation) -> Union[RoleState, None]:
        """get_situation_role(sim_info, situation)

        Get the current Situation Role a Sim is assigned to in a Situation.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param situation: A situation.
        :type situation: Situation
        :return: The Situation Role the Sim is assigned to in the Situation or None if the Sim is not running the Situation.
        :rtype: RoleState or None
        """
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return None
        return situation.get_current_role_state_for_sim(sim)
