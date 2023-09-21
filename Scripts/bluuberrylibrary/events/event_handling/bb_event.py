"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity


class BBEvent:
    def __init__(self, mod_identity: BBModIdentity):
        self._mod_identity = mod_identity

    @property
    def mod_identity(self) -> BBModIdentity:
        """The identity of the mod dispatching this event."""
        return self._mod_identity
