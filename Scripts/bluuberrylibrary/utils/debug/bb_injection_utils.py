"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import os
from functools import wraps
from typing import Any, Callable

from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from sims4.utils import flexmethod

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'


class _ClassForTypeChecking:
    @classmethod
    def class_method(cls):
        pass

    def self_method(self):
        pass

    # noinspection PyMethodParameters
    @flexmethod
    def flex_method(cls, inst):
        pass

    # noinspection PyPropertyDefinition
    @property
    def property_type(self):
        pass

    @staticmethod
    def static_method():
        pass


ClassMethodType = type(_ClassForTypeChecking.class_method)
SelfMethodType = type(_ClassForTypeChecking.self_method)
StaticMethodType = type(_ClassForTypeChecking.static_method)
FlexMethodType = type(_ClassForTypeChecking.flex_method)
PropertyType = type(_ClassForTypeChecking.property_type)


class BBInjectionUtils:
    """Utilities to inject custom functionality into functions.

    """
    @staticmethod
    def inject(mod_identity: BBModIdentity, target_object: Any, target_name: str, log_errors: bool = True) -> Callable:
        """inject(mod_identity, target_object, target_name, log_errors=True)

        A decorator used to inject code into a function.
        It will run the original function should any problems occur.
        If log_errors is True, it will catch and log exceptions.

        :Example of cls usage:

        .. highlight:: python
        .. code-block:: python

            # cls usage
            @BBInjectionUtils.inject(ModIdentity(), SimSpawner, SimSpawner.spawn_sim.__name__)
            def do_something_on_spawn_sim(original, cls, *args, **kwargs):
                return original(*args, **kwargs)

        :Example of self usage:

        .. highlight:: python
        .. code-block:: python

            # Self usage
            @BBInjectionUtils.inject(ModIdentity(), SimInfo, 'load_sim_info')
            def do_something_on_load_sim_info(original, self, *args, **kwargs):
                return original(self, *args, **kwargs)

        .. note::

           Injection WILL work on

           - Functions decorated with 'property'
           - Functions decorated with 'classmethod'
           - Functions decorated with 'staticmethod'
           - Functions decorated with 'flexmethod'
           - Functions with 'cls' or 'self' as the first argument.

        .. note::

           Injection WILL NOT work on

           - Global functions, i.e. Functions not contained within a class.
           - Global variables, i.e. Variables not contained within a class or function.
           - Functions decorated with 'classproperty'
           - Functions decorated with 'staticproperty'
           - Functions decorated with 'flexproperty'

        :param mod_identity: The identity of the Mod that is injecting custom code.
        :type mod_identity: BBModIdentity
        :param target_object: The class that contains the target function.
        :type target_object: Any
        :param target_name: The name of the function being injected to.
        :type target_name: str
        :param log_errors: If set to True, any errors thrown by the wrapped function will be handled by your mod. If set to False, any errors thrown by the wrapped function will not be caught. Default is True.
        :type log_errors: bool, optional
        :return: A wrapped function.
        :rtype: Callable
        """
        if ON_RTD:
            def _injected(wrap_function) -> Any:
                return wrap_function
            return _injected

        if log_errors:
            def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
                # noinspection PyBroadException
                try:
                    # @classmethod
                    if isinstance(original_function, ClassMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_class_function(cls, *args, **kwargs) -> Any:
                            try:
                                def _do_original(*_, **__):
                                    return original_function_func(cls, *_, **__)

                                return new_function(_do_original, cls, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
                                    BBLogRegistry().register_log(mod_identity, 'bb_injection_utils').error('Error occurred in function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function_func(cls, *args, **kwargs)

                        return classmethod(_wrapped_class_function)

                    # self method
                    if isinstance(original_function, SelfMethodType):
                        @wraps(original_function)
                        def _wrapped_self_function(self, *args, **kwargs) -> Any:
                            try:
                                return new_function(original_function, self, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
                                    BBLogRegistry().register_log(mod_identity, 'bb_injection_utils').error('Error occurred in function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function(self, *args, **kwargs)

                        return _wrapped_self_function

                    # @property
                    if isinstance(original_function, PropertyType):
                        # noinspection PyTypeChecker
                        @wraps(original_function)
                        def _wrapped_property_function(self, *args, **kwargs) -> Any:
                            try:
                                return new_function(original_function.fget, self, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
                                    BBLogRegistry().register_log(mod_identity, 'bb_injection_utils').error('Error occurred in function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function(self, *args, **kwargs)

                        return property(_wrapped_property_function)

                    if isinstance(original_function, StaticMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_static_function(*args, **kwargs) -> Any:
                            try:
                                def _do_original(*_, **__):
                                    return original_function_func(*_, **__)

                                return new_function(_do_original, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
                                    BBLogRegistry().register_log(mod_identity, 'bb_injection_utils').error('Error occurred in function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function_func(*args, **kwargs)

                        return staticmethod(_wrapped_static_function)

                    if isinstance(original_function, FlexMethodType):
                        def _wrapped_flex_function(cls, inst, *args, **kwargs) -> Any:
                            try:
                                def _do_original(*_, **__):
                                    return original_function.func(cls, inst, *_, **__)

                                return new_function(_do_original, cls, inst, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
                                    BBLogRegistry().register_log(mod_identity, 'bb_injection_utils').error('Error occurred in function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function.func(cls, inst, *args, **kwargs)

                        _wrapped_flex_function.__name__ = target_name

                        return flexmethod(_wrapped_flex_function)

                    # Other thing
                    @wraps(original_function)
                    def _wrapped_function(*args, **kwargs) -> Any:
                        try:
                            return new_function(original_function, *args, **kwargs)
                        except Exception as ex:
                            # noinspection PyBroadException
                            try:
                                from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
                                BBLogRegistry().register_log(mod_identity, 'bb_injection_utils').error('Error occurred in function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                            except Exception:
                                pass
                            return original_function(*args, **kwargs)

                    return _wrapped_function
                except:
                    def _func(*_, **__) -> Any:
                        pass
                    return _func
        else:
            def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
                # @classmethod
                if isinstance(original_function, ClassMethodType):
                    original_function_func = original_function.__func__

                    # noinspection PyDecorator
                    @wraps(original_function)
                    def _wrapped_class_function(cls, *args, **kwargs) -> Any:
                        def _do_original(*_, **__):
                            return original_function_func(cls, *_, **__)

                        return new_function(_do_original, cls, *args, **kwargs)

                    return classmethod(_wrapped_class_function)

                # self method
                if isinstance(original_function, SelfMethodType):
                    @wraps(original_function)
                    def _wrapped_self_function(self, *args, **kwargs) -> Any:
                        return new_function(original_function, self, *args, **kwargs)

                    return _wrapped_self_function

                # @property
                if isinstance(original_function, PropertyType):
                    # noinspection PyTypeChecker
                    @wraps(original_function)
                    def _wrapped_property_function(self, *args, **kwargs) -> Any:
                        return new_function(original_function.fget, self, *args, **kwargs)

                    return property(_wrapped_property_function)

                if isinstance(original_function, StaticMethodType):
                    original_function_func = original_function.__func__

                    # noinspection PyDecorator
                    @wraps(original_function)
                    def _wrapped_static_function(*args, **kwargs) -> Any:
                        def _do_original(*_, **__):
                            return original_function_func(*_, **__)

                        return new_function(_do_original, *args, **kwargs)

                    return staticmethod(_wrapped_static_function)

                if isinstance(original_function, FlexMethodType):
                    def _wrapped_flex_function(cls, inst, *args, **kwargs) -> Any:
                        def _do_original(*_, **__):
                            return original_function.func(cls, inst, *_, **__)

                        return new_function(_do_original, cls, inst, *args, **kwargs)

                    _wrapped_flex_function.__name__ = target_name

                    return flexmethod(_wrapped_flex_function)

                @wraps(original_function)
                def _wrapped_function(*args, **kwargs) -> Any:
                    return new_function(original_function, *args, **kwargs)
                return _wrapped_function

        def _injected(_wrap_function) -> Any:
            _original_function = getattr(target_object, str(target_name))
            setattr(target_object, str(target_name), _function_wrapper(_original_function, _wrap_function))
            return _wrap_function

        return _injected
