""" Backend abstraction """
from courseware.access import has_access
from courseware.courses import get_course_with_access


def get_has_access(*args, **kwargs):
    """
    """
    return has_access(*args, **kwargs)


def course_with_access(*args, **kwargs):
    """
    """
    return get_course_with_access(*args, **kwargs)
