"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.events.event_dispatchers.bb_event_dispatcher import BBEventDispatcher
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_despawned_event import BBOnSimDespawnedEvent
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_spawned_event import BBOnSimSpawnedEvent
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner


class BBSimEventDispatcher(BBEventDispatcher):
    """Dispatches event related to Sims"""

    def __init__(self):
        super().__init__()

    def on_sim_spawned(self, sim_info: SimInfo) -> BBRunResult:
        """on_sim_spawned(sim_info)

        Dispatch an event when a Sim spawns.

        :return: The result of dispatching the event. True, if successful. False, if not.
        :rtype: BBTestResult
        """
        event = BBOnSimSpawnedEvent(ModIdentity(), sim_info)
        return self.dispatch(event)

    def on_sim_despawned(self, sim_info: SimInfo) -> BBRunResult:
        """on_sim_despawned(sim_info)

        Dispatch an event when a Sim despawns.

        :return: The result of dispatching the event. True, if successful. False, if not.
        :rtype: BBTestResult
        """
        event = BBOnSimDespawnedEvent(ModIdentity(), sim_info)
        return self.dispatch(event)


@BBInjectionUtils.inject(ModIdentity(), SimSpawner, SimSpawner.spawn_sim.__name__, log_errors=False)
def _bbl_on_sim_spawned(original, cls, sim_info, *args, **kwargs):
    result = original(sim_info, *args, **kwargs)
    BBSimEventDispatcher().on_sim_spawned(sim_info)
    return result


@BBInjectionUtils.inject(ModIdentity(), Sim, Sim.destroy.__name__, log_errors=False)
def _bbl_on_sim_despawned(original, self, *args, **kwargs):
    sim_info = BBSimUtils.to_sim_info(self)
    BBSimEventDispatcher().on_sim_despawned(sim_info)
    result = original(self, *args, **kwargs)
    return result
