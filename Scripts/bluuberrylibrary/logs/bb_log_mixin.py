"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.logs.bb_log import BBLog
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity


class BBLogMixin:
    """A mixin that provides functions for creating and maintaining a log."""
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        """The identity of the mod that owns this class."""
        raise NotImplementedError()

    @classmethod
    def get_log_name(cls) -> str:
        """The name of the log used within the class."""
        raise NotImplementedError()

    @classmethod
    def get_log(cls) -> BBLog:
        """Get an instance of the class owned log."""
        return BBLogRegistry().register_log(cls.get_mod_identity(), cls.get_log_name())