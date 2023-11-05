from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.utils.instances.bb_instance_utils import BBInstanceUtils
from bluuberrylibrary.utils.sims.bb_sim_spawn_utils import BBSimSpawnUtils
from sims.sim_info_types import SpeciesExtended, Gender, Age
from sims4.commands import CommandType, Command

log = BBLogRegistry().register_log(ModIdentity(), 'bbl_sim_spawn_commands')


@Command(
    'bbl.spawn_sim',
    command_type=CommandType.Live
)
def _bbl_command_spawn_sim(species: str = 'human', gender: str = 'male', age: str = 'adult', _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    species_val = BBInstanceUtils.get_enum_from_name(species.upper(), SpeciesExtended, default_value=None)
    if species_val is None:
        output(f'Incorrect value for Species {species}')
        return False
    gender_val = BBInstanceUtils.get_enum_from_name(gender.upper(), Gender, default_value=None)
    if gender_val is None:
        output(f'Incorrect value for Gender {gender}')
        return False
    age_val = BBInstanceUtils.get_enum_from_name(age.upper(), Age, default_value=None)
    if age_val is None:
        output(f'Incorrect value for Age {age}')
        return False
    output(f'Creating Sim {species_val}, {gender_val}, {age_val}')
    try:
        created_sim_info = BBSimSpawnUtils.create_sim_info(species_val, gender=gender_val, age=age_val)
        BBSimSpawnUtils.spawn_sim(created_sim_info)
        output('Done')
    except Exception as ex:
        output(f'An error occurred {ex}')
        log.error('Error occurred spawning Sim', exception=ex)
