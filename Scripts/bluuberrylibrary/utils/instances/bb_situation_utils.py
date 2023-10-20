"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from role.role_state import RoleState
from situations.situation import Situation
from situations.situation_job import SituationJob


class BBSituationUtils:
    """Utilities for managing Situations."""

    @classmethod
    def get_situation_guid(cls, situation: Situation) -> int:
        """get_situation_guid(situation)

        Get the GUID of a Situation.

        :param situation: A situation.
        :type situation: Situation
        :return: The GUID of the Situation or -1 if not found.
        :rtype: int
        """
        if situation is None:
            return -1
        return getattr(situation, 'guid64', -1)

    @classmethod
    def get_situation_name(cls, situation: Situation) -> str:
        """get_situation_name(situation)

        Get the Tuning name of a situation.

        :param situation: A situation.
        :type situation: Situation
        :return: The tuning name of the situation or "No Situation Name" if not found.
        :rtype: str
        """
        if situation is None or not hasattr(situation, '__class__'):
            return 'No Situation Name'
        return situation.__class__.__name__ or 'No Situation Name'

    @classmethod
    def get_situation_job_name(cls, situation_job: SituationJob) -> str:
        """get_situation_job_name(situation_job)

        Get the Tuning name of a Situation Job.

        :param situation_job: A situation job.
        :type situation_job: SituationJob
        :return: The tuning name of the situation or "No Situation Job Name" if not found.
        :rtype: str
        """
        if situation_job is None or not hasattr(situation_job, '__name__'):
            return 'No Situation Job Name'
        return situation_job.__name__ or 'No Situation Job Name'

    @classmethod
    def get_situation_role_name(cls, situation_role: RoleState) -> str:
        """get_situation_role_name(situation_role)

        Get the Tuning name of a Situation Role.

        :param situation_role: A situation role.
        :type situation_role: RoleState
        :return: The tuning name of the situation or "No Situation Role Name" if not found.
        :rtype: str
        """
        if situation_role is None or not hasattr(situation_role, '__name__'):
            return 'No Situation Role Name'
        return situation_role.__name__ or 'No Situation Role Name'
