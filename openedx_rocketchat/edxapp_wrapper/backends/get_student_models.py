""" Backend abstraction """
from student.models import (  # pylint: disable=import-error
    CourseEnrollment,
    CourseEnrollmentManager,
    anonymous_id_for_user,
    get_user
)


def get_course_enrollment():
    """ Backend to CourseEnrollment """
    return CourseEnrollment


def get_course_enrollment_manager():
    """ Backend to CourseEnrollmentManager """
    return CourseEnrollmentManager


def get_anonymous_id_for_edxapp_user(*args, **kwargs):  # pylint: disable=invalid-name
    """ Backend to get anonymous_id_for_user """
    return anonymous_id_for_user(*args, **kwargs)


def get_edxapp_user(*args, **kwargs):
    """ Backend to get_user """
    return get_user(*args, **kwargs)
