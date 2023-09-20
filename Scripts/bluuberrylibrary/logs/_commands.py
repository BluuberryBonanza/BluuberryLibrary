"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.mod_identity import ModIdentity
from sims4.commands import Command, CommandType


@Command(
    'bbl.enable_log',
    # 'Enable a log. Once enabled, the log will write messages to "The Sims 4/bb_logs/modname_version_Debug.txt"',
    command_type=CommandType.Live
)
def _bbl_command_enable_log(log_name: str, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    if log_name is None:
        output('ERROR: No log name specified.')
        return
    output(f'Attempting to enable log \'{log_name}\'.')
    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
    if BBLogRegistry().enable_logs(log_name):
        output(f'SUCCESS: Log \'{log_name}\' was successfully enabled.')
    else:
        output(f'FAILED: Failed to enable log \'{log_name}\'.')


@Command(
    'bbl.disable_log',
    # 'Disable a log. Once disabled, the log will no longer write any messages.',
    command_type=CommandType.Live
)
def _bbl_command_disable_log(log_name: str, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    if log_name is None:
        output('No log name specified!')
        return
    output(f'Attempting to disable log \'{log_name}\'.')
    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
    if BBLogRegistry().disable_logs(log_name):
        output(f'SUCCESS: Log \'{log_name}\' was successfully disabled.')
    else:
        output(f'Failed to disable log \'{log_name}\'.')


@Command('bbl.test_log', command_type=CommandType.Live)
def _bbl_command_test_log(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Testing log')
    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
    _bb_base_log = BBLogRegistry().register_log(ModIdentity(), 'bb_log_registry')
    _bb_base_log.enable()
    _bb_base_log.debug('Wrote a message, does it appear?')
    _bb_base_log.disable()
    output('Done testing log')