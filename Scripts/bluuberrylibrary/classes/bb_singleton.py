"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import TypeVar

SingletonType = TypeVar('SingletonType', bound=object)


class BBSingleton(type):
    """Any instances created using this class will be of a single instance.

    Usage: class Foo(metaclass=BBSingleton):

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        class Foo(metaclass=BBSingleton):
            def __init__(self):
                self.state = 0

        f = Foo()
        f.state = 3
        g = Foo()
        g.state == 3  # True

    """
    def __init__(cls, *args, **kwargs) -> None:
        super(BBSingleton, cls).__init__(*args, **kwargs)
        cls._instances = {}

    def __call__(cls, *args, **kwargs) -> 'BBSingleton':
        if cls not in cls._instances:
            cls._instances[cls] = super(BBSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
