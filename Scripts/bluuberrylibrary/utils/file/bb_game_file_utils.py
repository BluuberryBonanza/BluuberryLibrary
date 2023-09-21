"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import os


class BBGameFileUtils:
    """Utilities for reading/writing game related files.

    """
    @classmethod
    def get_the_sims_4_file_path(cls) -> str:
        """get_the_sims_4_file_path()

        Retrieve the full path of the folder 'Documents\\Electronic Arts\\The Sims 4'

        :return: The file path to 'Documents\\Electronic Arts\\The Sims 4' folder.
        :rtype: str
        """
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_file_path.partition(f"{os.sep}Mods{os.sep}")[0])
