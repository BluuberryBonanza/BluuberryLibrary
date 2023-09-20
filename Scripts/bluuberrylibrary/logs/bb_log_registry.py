"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import os
from typing import Dict

from bluuberrylibrary.logs.bb_log import BBLog
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.services.bb_singleton import BBSingleton

_bb_base_log = None


class BBLogRegistry(BBSingleton):
    """BBLogRegistry()

    Used to create and register logs.

    :Example Usage:

    .. highlight:: python
    .. code-block:: python

        # Register the log, Logs will appear in a file titled "MOD_NAME_version_Debug.txt" and messages logged using this log will be prefixed with "bbl_log_name"
        log = BBLogRegistry().register_log(ModIdentity(), 'bbl_log_name')
        # Enable the log, if not enabled, messages will not be logged.
        log.enable()
        # Log a message
        log.debug('This is dummy text.')
        # Disable the log
        log.disable()

        # The BluuberryLibrary_v1.0_Debug.txt file will contain the "This is dummy text." message.

    .. note::

        Available Commands:

        - `bbl.enable_log` or `bbl.enablelog`
        - `bbl.disable_log` or `bbl.disablelog`
        - `bbl.disable_all_logs` or `bbl.disablealllogs`
        - `bbl.logs`

    """
    def __init__(self) -> None:
        self._registered_logs: Dict[str, Dict[str, BBLog]] = dict()
        self._delete_old_log_files()

    @classmethod
    def _logging_folder_path(cls) -> str:
        from bluuberrylibrary.utils.file.bb_file_utils import BBFileUtils
        return os.path.join(BBFileUtils.get_the_sims_4_file_path(), 'bb_logs')

    def _delete_old_log_files(self) -> None:
        from bluuberrylibrary.utils.file.bb_file_utils import BBFileUtils
        files_to_delete = (
            self._logging_folder_path(),
        )
        for file_to_delete in files_to_delete:
            # noinspection PyBroadException
            try:
                if os.path.isfile(file_to_delete):
                    BBFileUtils.delete_file(file_to_delete, ignore_errors=True)
                else:
                    BBFileUtils.delete_directory(file_to_delete, ignore_errors=True)
            except:
                continue

    # noinspection PyUnusedLocal
    def enable_logs(self, log_name: str, mod_identity: BBModIdentity = None) -> bool:
        """enable_logs(log_name, mod_identity=None)

        Enable all logs with the specified name. If a mod identity is specified, only logs registered to that mod will be enabled. Otherwise, all logs with the same name will be enabled.

        :param log_name: The name of the logs to enable.
        :type log_name: str
        :param mod_identity: The identity of the mod the log belongs to. Default is None.
        :type mod_identity: BBModIdentity, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        if mod_identity is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                log = self._registered_logs[log_mod_name][log_name]
                log.enable()
        else:
            mod_name = mod_identity.mod_name.lower()
            if mod_name not in self._registered_logs:
                return False
            if log_name not in self._registered_logs[mod_name]:
                log = self.register_log(mod_identity, log_name)
                if log is not None:
                    log.enable()
                    return True
                return False
            self._registered_logs[mod_name][log_name].enable()
        return True

    # noinspection PyUnusedLocal
    def disable_logs(self, log_name: str, mod_identity: BBModIdentity = None) -> bool:
        """disable_logs(log_name, mod_identity=None)

        Disable all logs with the specified name. If a mod identity is specified, only logs registered to that mod will be disabled. Otherwise, all logs with the same name will be disabled.

        :param log_name: The name of the logs to disable.
        :type log_name: str
        :param mod_identity: The identity of the mod the log belongs to. Default is None.
        :type mod_identity: BBModIdentity, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        if mod_identity is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                log = self._registered_logs[log_mod_name][log_name]
                log.disable()
        else:
            mod_name = mod_identity.mod_name.lower()
            if mod_name not in self._registered_logs:
                return False
            if log_name not in self._registered_logs[mod_name]:
                return False
            self._registered_logs[mod_name][log_name].disable()
        return True

    def register_log(
        self,
        mod_identity: BBModIdentity,
        log_name: str,
        override_logging_path: str = None
    ) -> BBLog:
        """register_log(mod_identity, log_name, override_logging_path=None)

        Create and register a log with the specified name.

        .. note:: If `log_name` matches the name of a Log already registered, that log will be returned rather than creating a new Log.

        :param mod_identity: The identity of the mod registering a log.
        :type mod_identity: BBModIdentity
        :param log_name: The name of the log.
        :type log_name: str
        :param override_logging_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
        :type override_logging_path: str, optional
        :return: A log.
        :rtype: BBLog
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        mod_name = mod_identity.mod_name.lower()
        first_time_log = False
        # Dict[str, Dict[str, BBLog]]
        if mod_name not in self._registered_logs:
            first_time_log = True
            self._registered_logs[mod_name] = dict()
        # Dict[str, BBLog]
        if log_name in self._registered_logs[mod_name]:
            return self._registered_logs[mod_name][log_name]
        log = BBLog(mod_identity, log_name, logging_file_path=override_logging_path)
        self._registered_logs[mod_name][log_name] = log
        if first_time_log and mod_identity is not None and _bb_base_log is not None:
            _bb_base_log.enable()
            _bb_base_log.debug(f'{mod_identity} Detected.')
            _bb_base_log.disable()
        return log


# noinspection PyRedeclaration
_bb_base_log = BBLogRegistry().register_log(ModIdentity(), 'bb_log_registry')
