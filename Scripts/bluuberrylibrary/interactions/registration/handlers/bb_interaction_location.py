"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from enum import Int


class BBInteractionLocation(Int):
    """Different locations for which interactions exist."""
    TERRAIN: 'BBInteractionLocation' = ...
    OCEAN: 'BBInteractionLocation' = ...
    SCRIPT_OBJECT: 'BBInteractionLocation' = ...
    RELATIONSHIP_PANEL: 'BBInteractionLocation' = ...
    PHONE: 'BBInteractionLocation' = ...
