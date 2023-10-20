"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable

from bluuberrylibrary.classes.bb_run_result import BBRunResult
from objects.game_object import GameObject
from objects.object_enums import ItemLocation
from sims4.math import Location


class BBObjectSpawnUtils:
    """Utilities for creating and spawning Game Objects."""

    @classmethod
    def create_object(
        cls,
        object_definition: int,
        on_init: Callable[[GameObject], None] = None,
        on_added: Callable[[GameObject], None] = None,
        item_location: ItemLocation = ItemLocation.ON_LOT,
        **kwargs
    ) -> GameObject:
        """create_object(\
            object_definition,\
            on_init=None,\
            on_added=None,\
            item_location=ItemLocation.ON_LOT,\
            **kwargs\
        )

        Create a Game Object from an Object Definition.

        :param object_definition: The Object Definition to create the Game Object from.
        :type object_definition: int
        :param on_init: Occurs when the object is initialized. Default is None.
        :type on_init: Callable[[GameObject], None], optional
        :param on_added: Occurs when the object is added to the Object Manager for the specified item_location. Default is nothing.
        :type on_added: Callable[[GameObject], None], optional
        :param item_location: The location to spawn the object at. Default is ON_LOT.
        :type item_location: ItemLocation, optional
        :return: The created Game Object.
        :rtype: GameObject
        """
        from objects.system import create_object
        return create_object(
            object_definition,
            init=on_init,
            post_add=on_added,
            loc_type=item_location,
            **kwargs
        )

    @classmethod
    def spawn_object_at_location(
        cls,
        object_definition: int,
        location: Location,
        on_init: Callable[[GameObject], None] = None,
        on_added: Callable[[GameObject], None] = None,
        **kwargs
    ) -> BBRunResult:
        """spawn_object_at_location(\
            object_definition,\
            location,\
            on_init=None,\
            on_added=None,\
            **kwargs\
        )

        Create and Spawn an Object at a Location.

        :param object_definition: The Object Definition to create the Game Object from.
        :type object_definition: int
        :param location: The location to place the Game Object once it is spawned.
        :type location: Location
        :param on_init: Occurs when the object is initialized. Default is None.
        :type on_init: Callable[[GameObject], None], optional
        :param on_added: Occurs when the object is added to the Object Manager for the specified item_location. Default is nothing.
        :type on_added: Callable[[GameObject], None], optional
        :return: The spawned object or None if an issue occurs.
        :rtype: BBRunResult[GameObject]
        """
        object_instance = cls.create_object(
            object_definition,
            on_init=on_init,
            on_added=on_added,
            **kwargs
        )
        if object_instance is None:
            return BBRunResult(None, 'Failed to create the object.')
        object_instance.location = location
        return BBRunResult(object_instance, 'Successfully created the object')
