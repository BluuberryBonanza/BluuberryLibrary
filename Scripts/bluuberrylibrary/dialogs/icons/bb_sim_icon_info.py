"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from bluuberrylibrary.dialogs.icons.bb_icon_info import BBIconInfo
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim import Sim
from sims.sim_info import SimInfo


class BBSimIconInfo(BBIconInfo):
    """BBSimIconInfo(sim_info)

    Use this when you want an icon to be for a Sim.

    .. note:: This icon only works when the Sim is currently spawned.

    :param sim_info: The SimInfo, Sim ID, or Sim instance of a Sim.
    :type sim_info: SimInfo or Sim or int
    """
    def __init__(
        self,
        sim_info: Union[SimInfo, Sim, int]
    ):
        sim = BBSimUtils.to_sim_instance(sim_info)
        super().__init__(obj_instance=sim)
