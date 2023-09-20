"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import TypeVar

SingletonType = TypeVar('SingletonType', bound=object)


class _Singleton(type):
    def __init__(cls, *args, **kwargs) -> None:
        super(_Singleton, cls).__init__(*args, **kwargs)
        cls._instances = {}

    def __call__(cls, *args, **kwargs) -> 'BBSingleton':
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BBSingleton(metaclass=_Singleton):
    """Any instances created using this class will be of a single instance.


    :Example usage:

    .. highlight:: python
    .. code-block:: python

        class Foo(BBSingleton):
            def __init__(self):
                self.state = 0

        f = Foo()
        f.state = 3
        g = Foo()
        g.state == 3  # True

    """
    pass
