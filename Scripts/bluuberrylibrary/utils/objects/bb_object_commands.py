"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.utils.objects.bb_object_spawn_utils import BBObjectSpawnUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from event_testing.results import TestResult
from sims4.commands import CommandType, Command

log = BBLogRegistry().register_log(ModIdentity(), 'bbl_object_commands')


@Command(
    'bbl.spawn_object',
    command_type=CommandType.Live
)
def _bbl_command_spawn_object(object_definition: int, _connection: int = None):
    active_sim_info = None
    active_sim_location = None
    object_instance = None
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    try:
        output(f'Creating Object from {object_definition} and placing it at the feet of the active Sim.')
        active_sim_info = BBSimUtils.get_active_sim_info()
        if active_sim_info is None:
            output('Failed, No active Sim Info found!')
            return TestResult(False, 'No Active Sim Info found!')
        active_sim_location = BBSimUtils.to_sim_instance(active_sim_info).location
        object_instance = BBObjectSpawnUtils.spawn_object_at_location(object_definition, active_sim_location)
        output(f'Done! {object_instance.result}')
    except Exception as ex:
        output('Failed to spawn object, an error occurred!')
        log.error(f'Failed to spawn object {object_definition}. An error occurred.', active_sim_info=active_sim_info, active_sim_location=active_sim_location, object_instance=object_instance, exception=ex)
        return TestResult(False, 'An error occurred.')
    return TestResult.TRUE
