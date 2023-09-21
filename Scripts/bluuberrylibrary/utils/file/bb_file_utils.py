"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import os
import shutil
from typing import Union


class BBFileUtils:
    """Utilities for reading/writing files.

    """
    @classmethod
    def delete_file(cls, file_path: str, ignore_errors: bool = False) -> bool:
        """delete_file(file_path, ignore_errors=False)

        Delete a file.

        :param file_path: The file to delete.
        :type file_path: str
        :param ignore_errors: If True, any exceptions thrown will be ignored (Useful in preventing infinite loops). Default is False.
        :type ignore_errors: bool, optional
        :return: True if successful. False if not.
        :rtype: bool
        """
        if file_path is None:
            return False
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as ex:
            if ignore_errors:
                return False
            raise ex
        return True

    @classmethod
    def delete_directory(cls, directory_path: str, ignore_errors: bool = False) -> bool:
        """delete_directory(directory_path, ignore_errors=False)

        Delete a directory.

        :param directory_path: The directory to delete.
        :type directory_path: str
        :param ignore_errors: If True, any exceptions thrown will be ignored (Useful in preventing infinite loops). Default is False.
        :type ignore_errors: bool, optional
        :return: True if successful. False if not.
        :rtype: bool
        """
        if directory_path is None:
            return False
        try:
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
        except Exception as ex:
            if ignore_errors:
                return False
            raise ex
        return True

    @classmethod
    def write_file(
        cls,
        file_path: str,
        text: str,
        buffering: int = 1,
        encoding: str = 'utf-8',
        ignore_errors: bool = False,
        remove_if_exists: bool = False
    ) -> bool:
        """write_file(\
            file_path,\
            text,\
            buffering=1,\
            encoding='utf-8',\
            ignore_errors=False,\
            remove_if_exists=False\
        )

        Write text to a file.

        :param file_path: The file to write to.
        :type file_path: str
        :param text: The text to write.
        :type text: str
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :param ignore_errors: If True, any exceptions thrown will be ignored (Useful in preventing infinite loops)
        :type ignore_errors: bool, optional
        :param remove_if_exists: If True and the File exists already, it will be deleted before writing the data. If False and the File exists already, the data will be appended to the end of it. Default is False.
        :type remove_if_exists: bool, optional
        :return: True if successful. False if not.
        :rtype: bool
        """
        if file_path is None or text is None:
            return False
        try:
            if remove_if_exists:
                cls.delete_file(file_path, ignore_errors=ignore_errors)
            with open(file_path, mode='a', buffering=buffering, encoding=encoding) as opened_file:
                opened_file.write(text)
                opened_file.flush()
                opened_file.close()
        except Exception as ex:
            if ignore_errors:
                return False
            raise ex
        return True

    @classmethod
    def read_file(
        cls,
        file_path: str,
        buffering: int = 1,
        encoding: str = 'utf-8'
    ) -> Union[str, None]:
        """read_file(\
            file_path,\
            buffering=1,\
            encoding='utf-8'\
        )

        Read text from a file.

        :param file_path: The file to read from.
        :type file_path: str
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :return: The contents of the file as a string or None if an error occurred.
        :rtype: Union[str, None]
        """
        if not os.path.isfile(file_path):
            return None
        with open(file_path, mode='r', buffering=buffering, encoding=encoding) as file:
            return file.read()
