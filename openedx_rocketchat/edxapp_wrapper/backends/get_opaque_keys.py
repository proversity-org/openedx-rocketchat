""" Backend abstraction """
from opaque_keys.edx.keys import CourseKey


def get_course_from_string(*args, **kwargs):
    """
    """
    return CourseKey.from_string(*args, **kwargs)
