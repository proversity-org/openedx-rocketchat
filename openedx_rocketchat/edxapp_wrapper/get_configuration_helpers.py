""" Backend abstraction """
from importlib import import_module
from django.conf import settings


def get_configuration_helpers(*args, **kwargs):
    """ Get microsite settings """

    backend_function = settings.ROCKETCHAT_CONFIGURATION_HELPERS
    backend = import_module(backend_function)

    return backend.get_configuration_helpers(*args, **kwargs)
