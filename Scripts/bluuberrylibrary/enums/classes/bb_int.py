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
        __slots__ = {
            'name',
            'value',
            '_next_auto_value',
            '_get_unknown_value',
            '__invert__',
            '__xor__',
            '__or__',
            '__and__',
            '__sub__',
            '__add__',
            '__reduce__',
            '__repr__',
            '__str__'
        }
else:
    from enum import Int


class BBInt(Int):
    """A class to be used when creating your own Int Enums."""
    __slots__ = {
            'name',
            'value',
            '_next_auto_value',
            '_get_unknown_value',
            '__invert__',
            '__xor__',
            '__or__',
            '__and__',
            '__sub__',
            '__add__',
            '__reduce__',
            '__repr__',
            '__str__'
        }
