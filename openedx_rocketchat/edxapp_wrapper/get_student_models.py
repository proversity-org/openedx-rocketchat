""" Backend abstraction """
from importlib import import_module
from django.conf import settings


def get_course_enrollment(*args, **kwargs):
    """ Backend to CourseEnrollment """
    backend_function = settings.ROCKETCHAT_STUDENT_MODELS
    backend = import_module(backend_function)

    return backend.get_course_enrollment(*args, **kwargs)


def get_course_enrollment_manager(*args, **kwargs):
    """ Backend to CourseEnrollmentManager """
    backend_function = settings.ROCKETCHAT_STUDENT_MODELS
    backend = import_module(backend_function)

    return backend.get_course_enrollment_manager(*args, **kwargs)


def anonymous_id_for_user(*args, **kwargs):
    """ Backend to get anonymous_id_for_user """
    backend_function = settings.ROCKETCHAT_STUDENT_MODELS
    backend = import_module(backend_function)

    return backend.get_anonymous_id_for_edxapp_user(*args, **kwargs)


def get_user(*args, **kwargs):
    """ Backend to get_user """
    backend_function = settings.ROCKETCHAT_STUDENT_MODELS
    backend = import_module(backend_function)

    return backend.get_edxapp_user(*args, **kwargs)
