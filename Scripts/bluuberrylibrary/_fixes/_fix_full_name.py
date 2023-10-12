"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from sims.sim_info import SimInfo


@BBInjectionUtils.inject(ModIdentity(), SimInfo, 'full_name')
def _fix_full_name(original_fun, self: SimInfo, *_, **__):
    original_value = original_fun(self, *_, **__)
    if original_value == '':
        first_name = getattr(self, 'first_name', '')
        last_name = getattr(self, 'last_name', '')
        if first_name and last_name:
            return f'{first_name} {last_name}'
        elif first_name:
            return first_name
        elif last_name:
            return last_name
    return original_value
