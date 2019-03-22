""" Backend abstraction """
from importlib import import_module
from django.conf import settings


def get_course_from_string(*args, **kwargs):
    """
    """
    backend_function = settings.ROCKETCHAT_OPAQUE_KEYS
    backend = import_module(backend_function)

    return backend.get_course_from_string(*args, **kwargs)
