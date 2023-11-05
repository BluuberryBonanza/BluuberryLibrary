"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import os
from pprint import pformat
from typing import List

from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.logs.bb_stacktrace_utils import BBStacktraceUtils
from bluuberrylibrary.utils.file.bb_file_utils import BBFileUtils
from bluuberrylibrary.utils.time.bb_date_utils import BBDateTimeUtils


class BBLog:
    """BBLog(mod_identity, log_name, logging_file_path=None)

    A class used to log messages.

    :param mod_identity: The identity of the mod that owns the log.
    :type mod_identity: BBModIdentity
    :param log_name: The name of the log, used when enabling/disabling logs via commands
    :type log_name: str
    :param logging_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
    :type logging_file_path: str, optional
    """
    def __init__(self, mod_identity: BBModIdentity, log_name: str, logging_file_path: str = None):
        self._mod_identity = mod_identity
        self._log_name = log_name
        self._logging_file_path = logging_file_path
        self._is_enabled = False

    @property
    def name(self) -> str:
        """The identifier of this log.

        :return: A string identifier.
        :rtype: str
        """
        return self._log_name

    @property
    def mod_name(self) -> str:
        """The name of the mod that owns the log.

        :return: The name of the mod that owns the log
        :rtype: str
        """
        return self._mod_identity.mod_name

    def debug(
        self,
        message: str,
        ignore_enabled: bool = False,
        **kwargs
    ):
        """debug(message, ignore_enabled=False, **kwargs)

        Log a message.

        :param message: The message to log.
        :type message: str
        :param ignore_enabled: If True, the message will be logged without checking if the log is enabled. If False, the message will only log when the log is enabled. Default is False.
        :type ignore_enabled: bool, optional
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        if ignore_enabled or self.is_enabled():
            if kwargs:
                self._log_text('DEBUG', '{} {}'.format(message, pformat(kwargs)))
            else:
                self._log_text('DEBUG', message)

    def error(
        self,
        message: str,
        exception: Exception = None,
        stack_trace: List[str] = None,
        **kwargs
    ):
        """error(message, exception=None, stack_trace=None, **kwargs)

        Log an error.

        :param message: The message to log.
        :type message: str
        :param exception: The exception that occurred. Default is None.
        :type exception: Exception, None
        :param stack_trace: The stack trace leading to the exception, if not supplied, a stack trace will be gathered for you. Default is None.
        :type stack_trace: List[str], optional
        :param kwargs: Keyword Arguments to format into the error message.
        :type kwargs: Any
        """
        if kwargs:
            self._log_error('{} {}'.format(message, pformat(kwargs)), exception=exception, stack_trace=stack_trace)
        else:
            self._log_error(message, exception=exception, stack_trace=stack_trace)

    def log_stack(self) -> None:
        """log_stack()

        Log the current stack trace and the calling frames

        """
        if not self.is_enabled():
            return
        import inspect
        current_frame = inspect.currentframe()
        calling_frame = inspect.getouterframes(current_frame, 2)
        self.debug('StackTrace', stack_trace=calling_frame)

    def enable(self) -> None:
        """enable()

        Enable the log.
        """
        self._is_enabled = True

    def disable(self) -> None:
        """disable()

        Disable the log.
        """
        self._is_enabled = False

    def is_enabled(self) -> bool:
        """is_enabled()

        Determine if the log is enabled.

        :return: True, if the log is enabled. False, if not.
        :rtype: bool
        """
        return self._is_enabled

    def __logging_file_path(self) -> str:
        from bluuberrylibrary.utils.file.bb_game_file_utils import BBGameFileUtils
        if self._logging_file_path:
            return os.path.join(BBGameFileUtils.get_the_sims_4_file_path(), 'bb_logs', self._logging_file_path)
        return os.path.join(BBGameFileUtils.get_the_sims_4_file_path(), 'bb_logs')

    def _debug_file_name(self) -> str:
        return '{}_{}_Debug.txt'.format(self.mod_name, self._mod_identity.mod_version)

    def _error_file_name(self) -> str:
        return '{}_{}_Exceptions.txt'.format(self.mod_name, self._mod_identity.mod_version)

    def _log_text(self, message_type: str, message: str, file_name: str = None):
        current_date_time_str = BBDateTimeUtils.get_current_real_date_time_string()
        new_message = '{} {}: [{}]: {}\n'.format(current_date_time_str, message_type, self.name, message)
        # noinspection PyBroadException
        try:
            file_path = os.path.join(self.__logging_file_path(), file_name or self._debug_file_name())
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            BBFileUtils.write_file(file_path, new_message, ignore_errors=True)
        except Exception:
            pass

    def _log_error(self, message: str, file_name: str = None, exception: Exception = None, stack_trace: List[str] = None):
        # noinspection PyBroadException
        try:
            exceptions = stack_trace or BBStacktraceUtils.get_full_stack_trace()
            if exception is not None:
                stack_trace_message = '{}{} -> {}: {}\n'.format(''.join(exceptions), message, type(exception).__name__, exception)
            else:
                stack_trace_message = '{}{}\n'.format(''.join(exceptions), message)
            file_path = os.path.join(self.__logging_file_path(), file_name or self._error_file_name())
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            exception_traceback_text = '[{}] {} {}\n'.format(self.mod_name, BBDateTimeUtils.get_current_real_date_time_string(), stack_trace_message)
            BBFileUtils.write_file(file_path, exception_traceback_text, ignore_errors=True)
        except Exception:
            pass
