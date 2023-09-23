"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from objects import HiddenReasonFlag, ALL_HIDDEN_REASONS
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims.sim_info_manager import SimInfoManager


class BBSimUtils:
    """Utilities for manipulating Sims."""

    @classmethod
    def to_sim_id(cls, sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]) -> int:
        """to_sim_id(sim_identifier)

        Convert a Sim identifier to a Sim ID.

        :param sim_identifier: The identifier or instance of a Sim.
        :type sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
        :return: The decimal identifier for the Sim instance or 0 if a problem occurs.
        :rtype: int
        """
        if sim_identifier is None:
            return 0
        if isinstance(sim_identifier, int):
            return sim_identifier
        if isinstance(sim_identifier, Sim):
            return sim_identifier.sim_id
        if isinstance(sim_identifier, SimInfo):
            return sim_identifier.id
        if isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.id
        return 0

    @classmethod
    def to_sim_info(
        cls,
        sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
    ) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """to_sim_info(sim_identifier)

        Convert a Sim identifier to SimInfo.

        :param sim_identifier: The identifier or instance of a Sim to use.
        :type sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
        :return: The SimInfo of the specified Sim instance or None, if SimInfo is not found.
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        if sim_identifier is None or isinstance(sim_identifier, SimInfo):
            return sim_identifier
        if isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.get_sim_info()
        if isinstance(sim_identifier, Sim):
            return sim_identifier.sim_info
        if isinstance(sim_identifier, int):
            return cls.get_sim_info_manager().get(sim_identifier)
        return sim_identifier

    @classmethod
    def to_sim_instance(
        cls,
        sim_identifier: Union[int, Sim, SimInfo],
        allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS
    ) -> Union[Sim, None]:
        """to_sim_instance(sim_identifier, allow_hidden_flags=HiddenReasonFlag.NONE)

        Convert a Sim identifier to a Sim Instance.

        :param sim_identifier: The identifier or instance of a Sim.
        :type sim_identifier: Union[int, Sim, SimInfo]
        :param allow_hidden_flags: Flags to indicate the types of hidden Sims to consider as being instanced. Default is ALL_HIDDEN_REASONS
        :type allow_hidden_flags: HiddenReasonFlag, optional
        :return: The instance of the specified Sim or None if no instance was found.
        :rtype: Union[Sim, None]
        """
        if sim_identifier is None or isinstance(sim_identifier, Sim):
            return sim_identifier
        if isinstance(sim_identifier, SimInfo):
            return sim_identifier.get_sim_instance(allow_hidden_flags=allow_hidden_flags)
        if isinstance(sim_identifier, int):
            sim_info = cls.get_sim_info_manager().get(sim_identifier)
            if sim_info is None:
                return None
            return cls.to_sim_instance(sim_info, allow_hidden_flags=allow_hidden_flags)
        if isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.get_sim_instance(allow_hidden_flags=allow_hidden_flags)
        return sim_identifier

    @classmethod
    def get_sim_info_manager(cls) -> SimInfoManager:
        """get_sim_info_manager()

        Retrieve the manager that manages Sims.

        :return: The manager that manages Sims.
        :rtype: SimInfoManager
        """
        import services
        return services.sim_info_manager()
