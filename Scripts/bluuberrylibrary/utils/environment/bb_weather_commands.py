"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.utils.environment.bb_weather_utils import BBWeatherUtils
from sims4.commands import CommandType, Command


@Command(
    'bbl.trigger_weather',
    command_type=CommandType.Live
)
def _bbl_command_trigger_weather_event(weather_event: int, duration: int = 1, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output(f'Triggering weather {weather_event} for {duration} Sim hours')
    BBWeatherUtils.trigger_weather_event(weather_event, duration)

