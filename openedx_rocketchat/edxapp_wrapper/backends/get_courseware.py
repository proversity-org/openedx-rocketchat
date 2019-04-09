""" Backend abstraction """
from courseware.access import has_access  # pylint: disable=import-error
from courseware.courses import get_course_with_access  # pylint: disable=import-error


def get_has_access(*args, **kwargs):
    """ Backend to has_access """
    return has_access(*args, **kwargs)


def course_with_access(*args, **kwargs):
    """ Backend to get_course_with_acces """
    return get_course_with_access(*args, **kwargs)
