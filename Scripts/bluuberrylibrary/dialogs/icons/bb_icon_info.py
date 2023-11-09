"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from distributor.shared_messages import IconInfoData


class BBIconInfo:
    """BBIconInfo(\
        icon_resource=None,\
        obj_instance=None,\
        obj_def_id=None,\
        obj_geo_hash=None,\
        obj_material_hash=None,\
        obj_name=None\
    )

    Used as an alternative to IconInfoData directly.

    """
    def __init__(
        self,
        icon_resource=None,
        obj_instance=None,
        obj_def_id=None,
        obj_geo_hash=None,
        obj_material_hash=None,
        obj_name=None
    ):
        self.icon_resource = icon_resource
        self.obj_instance = obj_instance
        self.obj_def_id = obj_def_id
        self.obj_geo_hash = obj_geo_hash
        self.obj_material_hash = obj_material_hash
        self.obj_name = obj_name

    def to_icon(self) -> Union[IconInfoData, None]:
        """to_icon()

        Create an IconInfoData object from this instance.

        :return: The info data for an icon.
        :rtype: IconInfoData or None
        """
        if self.icon_resource is None and self.obj_instance is None and self.obj_def_id is None and self.obj_geo_hash is None and self.obj_material_hash is None and self.obj_name is None:
            return None
        return IconInfoData(
            icon_resource=self.icon_resource,
            obj_instance=self.obj_instance,
            obj_def_id=self.obj_def_id,
            obj_geo_hash=self.obj_geo_hash,
            obj_material_hash=self.obj_material_hash,
            obj_name=self.obj_name
        )
