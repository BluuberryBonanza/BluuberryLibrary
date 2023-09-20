"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from datetime import datetime


class BBDateTimeUtils:
    """A utility for managing date and time.

    """
    @classmethod
    def get_current_real_date_time(cls) -> datetime:
        """get_current_real_date_time()

        Retrieve the current date and time in Real Life.

        :return: The current real date and time in Real Life.
        :rtype: datetime
        """
        return datetime.now()

    @classmethod
    def get_current_real_date_time_string(cls) -> str:
        """get_current_real_date_time_string()

        Retrieve the current date in Real Life as a pre-formatted string.

        :return: The string representation of the current date and time in real life.
        :rtype: str
        """
        return str(cls.get_current_real_date_time().strftime('%Y-%m-%d %H:%M:%S.%f'))
