""" Backend abstraction """
from student.models import CourseEnrollment, CourseEnrollmentManager, anonymous_id_for_user, get_user


def get_course_enrollment():
    """
    """
    return CourseEnrollment


def get_course_enrollment_manager():
    """
    """
    return CourseEnrollmentManager


def get_anonymous_id_for_edxapp_user(*args, **kwargs):
    """
    """
    return anonymous_id_for_user(*args, **kwargs)


def get_edxapp_user(*args, **kwargs):
    """
    """
    return get_user(*args, **kwargs)
