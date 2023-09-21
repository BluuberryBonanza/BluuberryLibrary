"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.classes.bb_singleton import BBSingleton


class BBModIdentity(metaclass=BBSingleton):
    """Includes the identity of your mod.

    .. note:: It contains information about a mod such as Mod Name, Mod Author,\
        the module namespace, and the script file path to your mod.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity

        # This is how the bluuberrylibrary.mod_identity.ModIdentity implementation works.
        class ModIdentity(BBModIdentity):
            _FILE_PATH: str = str(__file__)

            @property
            def mod_name(self) -> str:
                return 'BluuberryLibrary'

            @property
            def mod_author(self) -> str:
                return 'BluuberryBonanza'

            @property
            def module_namespace(self) -> str:
                return 'bluuberrylibrary'

            @property
            def script_file_path(self) -> str:
                return ModIdentity._FILE_PATH

            @property
            def mod_version(self) -> str:
                return '1.0'

    """

    @property
    def mod_name(self) -> str:
        """The name of the mod.

        .. note:: Do not include spaces in the name!

        :return: The name of the mod.
        :rtype: str
        """
        raise NotImplementedError()

    @property
    def mod_author(self) -> str:
        """The one who made the mod.

        :return: The one who made the mod.
        :rtype: str
        """
        raise NotImplementedError()

    @property
    def module_namespace(self) -> str:
        """The namespace of the base module.

        .. note:: BBL would have a value of `bluuberrylibrary`.

        :return: The namespace of the base module.
        :rtype: str
        """
        raise NotImplementedError()

    @property
    def script_file_path(self) -> str:
        """The path to the .ts4script file of the mod.

        .. note::

           A good override value can be `__file__`, it will retrieve the file path automatically,\
           assuming the inheriting class is at the root of the mod.

        :return: The file path to the mod.
        :rtype: str
        """
        raise NotImplementedError()

    @property
    def mod_version(self) -> str:
        """The version the mod is currently at.

        :return: The version of the mod.
        :rtype: str
        """
        raise NotImplementedError()

    def __eq__(self, other: 'BBModIdentity') -> bool:
        if isinstance(other, str):
            return self.mod_name == other
        if not isinstance(other, BBModIdentity):
            return False
        return self.mod_name == other.mod_name

    def __hash__(self) -> int:
        return hash(self.mod_name)

    def __repr__(self) -> str:
        return 'mod_{}_version_{}_author_{}_namespace_{}'.format(self.mod_name, self.mod_version.replace('.', '_').replace('/', '_').replace('\\', '_'), self.mod_author, self.module_namespace)

    def __str__(self) -> str:
        return 'ModIdentity:\n Mod Name: {}\n Version: {}\n Mod Author: {}\n Module Namespace: {}\n Path To Mod: {}'.format(self.mod_name, self.mod_version, self.mod_author, self.module_namespace, self.script_file_path)

