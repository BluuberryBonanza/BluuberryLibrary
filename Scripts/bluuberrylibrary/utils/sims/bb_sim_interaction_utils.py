"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, Iterator

from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions.base.interaction import Interaction
from sims.sim_info import SimInfo


class BBSimInteractionUtils:
    """Utilities for manipulating interactions of Sims."""

    @classmethod
    def get_running_interactions_gen(cls, sim_info: SimInfo, include_interaction_callback: Callable[[Interaction], bool] = None) -> Iterator[Interaction]:
        """get_running_interactions_gen(sim_info, include_interaction_callback=None)

        Retrieve all interactions that a Sim is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, all interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterator of all running Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return tuple()
        if sim.si_state is None:
            return tuple()
        for interaction in tuple(sim.si_state):
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction

    @classmethod
    def get_queued_interactions_gen(cls, sim_info: SimInfo, include_interaction_callback: Callable[[Interaction], bool] = None) -> Iterator[Interaction]:
        """get_queued_interactions_gen(sim_info, include_interaction_callback=None)

        Retrieve all interactions that a Sim currently has queued.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, All interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterator of all queued Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return tuple()
        if sim.queue is None:
            return tuple()
        for interaction in tuple(sim.queue):
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction
