"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.logs.bb_log import BBLog
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from sims4.commands import Command, CommandType
from sims4.log import Logger


class _BBGameLogs(metaclass=BBSingleton):
    def __init__(self) -> None:
        self.logs_enabled = False
        self.game_log_identities = dict()
        self.logs = list()

    def get_log(self, log_name: str) -> BBLog:
        if log_name not in self.game_log_identities:
            class TempModIdentity(BBModIdentity):
                _FILE_PATH: str = str(__file__)

                @property
                def mod_name(self) -> str:
                    return log_name

                @property
                def mod_author(self) -> str:
                    return 'EA'

                @property
                def module_namespace(self) -> str:
                    return 'game'

                @property
                def script_file_path(self) -> str:
                    return self.__class__._FILE_PATH

                @property
                def mod_version(self) -> str:
                    return '1.0'

            mod_identity = TempModIdentity()
            self.game_log_identities[log_name] = mod_identity
        else:
            mod_identity = self.game_log_identities[log_name]

        _log = BBLogRegistry().register_log(mod_identity, f'log', override_logging_path='game_logs')
        _log.enable()
        self.logs.append(_log)
        return _log

    def _format_message(self, message, *args, owner=None, **__) -> str:
        to_log_message = message
        if args:
            to_log_message = to_log_message.format(*args)
        if owner:
            to_log_message = f'[{owner}] {to_log_message}'
        return to_log_message

    def enable_logs(self) -> None:
        self.logs_enabled = True

    def disable_logs(self) -> None:
        self.logs_enabled = False

    def _log(self, log_name: str, message: str, *args, level, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _BBGameLogs().get_log(log_name)
        to_log_message = _BBGameLogs()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug(f'{level}: {to_log_message}')

    def _debug(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _BBGameLogs().get_log(log_name)
        to_log_message = _BBGameLogs()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug(to_log_message)

    def _info(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _BBGameLogs().get_log(log_name)
        to_log_message = _BBGameLogs()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug(to_log_message)

    def _warn(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _BBGameLogs().get_log(log_name)
        to_log_message = _BBGameLogs()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug(to_log_message)

    def _error(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _BBGameLogs().get_log(log_name)
        to_log_message = _BBGameLogs()._format_message(message, *args, owner=owner, **kwargs)
        _log.error(to_log_message)

    def _exception(self, log_name: str, message: str, *args, exc: Exception = None, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _BBGameLogs().get_log(log_name)
        to_log_message = _BBGameLogs()._format_message(message, *args, owner=owner, **kwargs)
        _log.error(to_log_message, exception=exc, throw=True)


@Command(
    'bbl.enable_game_logs',
    command_type=CommandType.Live
)
def _bbl_command_enable_game_log(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Enabling the Game Logs.')
    if _BBGameLogs().logs_enabled:
        output('The Game Logs are already enabled.')
        return
    _BBGameLogs().enable_logs()
    output('Game Logs are now enabled.')


@Command(
    'bbl.disable_game_logs',
    command_type=CommandType.Live
)
def _bbl_disable_game_logs(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Disabling the Game Logs.')
    if not _BBGameLogs().logs_enabled:
        output('The Game Logs are already disabled.')
        return
    _BBGameLogs().disable_logs()
    output('Game Logs are now disabled.')


@BBInjectionUtils.inject(ModIdentity(), Logger, 'log', log_errors=False)
def _bbl_logger_log(original, self, message, *args, level, owner=None, **kwargs) -> Any:
    log_name = self.group
    _BBGameLogs()._log(log_name, message, *args, level, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, level, owner=owner, **kwargs)


@BBInjectionUtils.inject(ModIdentity(), Logger, 'debug', log_errors=False)
def _bbl_logger_debug(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _BBGameLogs()._debug(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@BBInjectionUtils.inject(ModIdentity(), Logger, 'info', log_errors=False)
def _bbl_logger_info(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _BBGameLogs()._info(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@BBInjectionUtils.inject(ModIdentity(), Logger, 'warn', log_errors=False)
def _bbl_logger_warn(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _BBGameLogs()._warn(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@BBInjectionUtils.inject(ModIdentity(), Logger, 'error', log_errors=False)
def _bbl_logger_error(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _BBGameLogs()._error(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@BBInjectionUtils.inject(ModIdentity(), Logger, 'exception', log_errors=False)
def _bbl_logger_exception(original, self, message, *args, exc=None, owner=None, **kwargs) -> Any:
    log_name = self.group
    _BBGameLogs()._exception(log_name, message, *args, exc=exc, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, exc=exc, owner=owner, **kwargs)
