"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from objects.game_object import GameObject
from sims4.math import Location


class BBObjectSpawnUtils:
    """Utilities for creating and spawning Game Objects."""

    @classmethod
    def create_object(cls, object_definition: int) -> GameObject:
        """create_object(object_definition_id)

        Create a Game Object from an Object Definition.

        :param object_definition: The Object Definition to create the Game Object from.
        :type object_definition: int
        :return: The created Game Object.
        :rtype: GameObject
        """
        from objects.system import create_object
        return create_object(object_definition)

    @classmethod
    def spawn_object_at_location(cls, object_definition: int, location: Location) -> Union[GameObject, None]:
        """spawn_object_at_location(object_definition, location)

        Create and Spawn an Object at a Location.

        :param object_definition: The Object Definition to create the Game Object from.
        :type object_definition: int
        :param location: The location to place the Game Object once it is spawned.
        :type location: Location
        :return: The spawned object, or None if an issue occurs.
        :rtype: GameObject or None
        """
        object_instance = cls.create_object(object_definition)
        if object_instance is None:
            return
        object_instance.location = location
        return object_instance
