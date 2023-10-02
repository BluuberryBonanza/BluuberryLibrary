"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import os

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if ON_RTD:
    class Int:
        pass
else:
    from enum import Int


class BBInt(Int):
    pass
