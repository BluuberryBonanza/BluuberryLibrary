# Configuration file for the Sphinx documentation builder.
import os
import sys

script_paths = [
    '../../Scripts/bluuberrylibrary'
]

sys.path.insert(0, os.path.abspath('../../Scripts'))
current_index = 1
for script_path in script_paths:
    for subdir, dirs, files in os.walk(script_path):
        if '__pycache__' in subdir:
            continue
        print(subdir)
        sys.path.insert(current_index, os.path.abspath(subdir))
        current_index += 1

# -- Project information

project = 'BluuberryLibrary'
copyright = '2023, BluuberryBonanza'
author = 'BluuberryBonanza'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'


autodoc_mock_imports = [
    'sims4', 'google', 'native', 'shared_commands', 'ui', 'cas', 'vet', 'vfx', 'fame', 'fire',
    'pets', 'plex', 'role', 'sims', 'audio', 'audio.voice', 'bucks', 'buffs', 'carry', 'clubs',
    'protocolbuffers', '_resourceman', 'enum', 'singletons', 'zone', 'clock', 'date_and_time', 'time_service',
    'scheduling', 'interactions', 'sims', 'paths', 'alarms', 'interactions.base.super_interaction',
    'interactions.base.immediate_interaction', 'interactions.base.interaction', 'interactions.base.mixer_interaction',
    'interactions.social.social_mixer_interaction', 'interactions.social.social_super_interaction',
    'tunable_utils', 'visualization', 'zone_modifier', 'call_to_action', 'celebrity_fans', 'lot_decoration',
    'drama_scheduler', 'global_policies', 'server_commands', 'story_progression', 'conditional_layers',
    'household_calendar', 'game_effect_modifier', 'household_milestones', 'open_street_director',
    'whims', 'world', 'curfew', 'relics', 'retail', 'server', 'spells', 'temple', 'topics', 'traits', 'trends',
    'venues', 'balloon', 'careers', 'filters', 'fishing', 'laundry', 'objects', 'rewards', 'routing',
    'primitives', 'reputation', 'situations', 'statistics', 'aspirations', 'constraints', 'distributor',
    'performance', 'rabbit_hole', 'reservation', 'restaurants', 'achievements', 'away_actions',
    'broadcasters', 'gsi_handlers', 'interactions', 'event_testing', 'relationships',
    'seasons', 'socials', 'weather', 'adoption', 'autonomy', 'business', 'crafting', 'delivery', 'ensemble',
    'holidays', 'notebook', 'postures', 'services', 'sickness', 'teleport', 'vehicles', 'animation', 'familiars',
    'headlines', 'narrative', 'tutorials', 'apartments', 'automation', 'households'
]

# -- Options for EPUB output
epub_show_urls = 'footnote'

add_module_names = False

master_doc = 'index'
autodoc_typehints = 'none'