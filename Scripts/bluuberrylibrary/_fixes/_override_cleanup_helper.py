"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from sims4.tuning.tunable_perf import TuningAttrCleanupHelper


@BBInjectionUtils.inject(ModIdentity(), TuningAttrCleanupHelper, 'register_for_cleanup')
def _fix_register_for_cleanup(original, self: TuningAttrCleanupHelper, *_, **__):
    if self._tracked_objects is None:
        self._tracked_objects = list()
    return original(self, *_, **__)
