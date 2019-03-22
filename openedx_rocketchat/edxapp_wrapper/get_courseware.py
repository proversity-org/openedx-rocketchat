""" Backend abstraction """
from importlib import import_module
from django.conf import settings


def has_access(*args, **kwargs):
    """
    """
    backend_function = settings.ROCKETCHAT_COURSEWARE
    backend = import_module(backend_function)

    return backend.get_has_access(*args, **kwargs)


def get_course_with_access(*args, **kwargs):
    """
    """
    backend_function = settings.ROCKETCHAT_COURSEWARE
    backend = import_module(backend_function)

    return backend.course_with_access(*args, **kwargs)
