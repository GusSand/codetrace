from typing import TypeAlias
__typ0 : TypeAlias = "ObjectDetectionAnnotation"
__typ1 : TypeAlias = "FaceRecognitionRectangle"
import json

from django.http import QueryDict
from django.utils import timezone

from ajapaik.ajapaik_face_recognition.models import FaceRecognitionRectangle
from ajapaik.ajapaik_object_recognition.models import ObjectDetectionAnnotation

DELETION_EXPIRATION_THRESHOLD_IN_HOURS = 24

GENDER_FEMALE = 0
GENDER_MALE = 1
GENDER_NOT_SURE = 2

GENDER_STRING_FEMALE = 'FEMALE'
GENDER_STRING_MALE = 'MALE'
GENDER_STRING_UNSURE = 'UNSURE'

AGE_CHILD = 0
AGE_ADULT = 1
AGE_ELDERLY = 2
AGE_NOT_SURE = 3

AGE_STRING_CHILD = 'CHILD'
AGE_STRING_ADULT = 'ADULT'
AGE_STRING_ELDERLY = 'ELDERLY'
AGE_STRING_UNSURE = 'UNSURE'


def __tmp13(val):
    return val is not None and len(val) > 0


def __tmp9(__tmp8):
    if __tmp13(__tmp8):
        return int(__tmp8)

    return 0


def __tmp6(__tmp7):
    query_dictionary = QueryDict('', mutable=True)
    query_dictionary.update(__tmp7)
    return query_dictionary


def __tmp11(user_id, __tmp12, transform_function, photo_id=None):
    transformed_collection = []

    for entry in __tmp12:
        transformed_collection.append(json.dumps(transform_function(entry, user_id).__dict__))
    return transformed_collection


def is_object_annotation_editable(user_id: int, __tmp0):
    created_on = __tmp0.created_on
    created_by_id = __tmp0.user_id

    return is_annotation_editable_for_user(user_id, created_on, created_by_id)


def __tmp5(user_id: <FILL>, annotation: __typ1):
    created_on = annotation.created
    created_by = annotation.user

    is_without_name = annotation.get_subject_name() is None
    is_created_by_system = created_by is None

    return is_without_name or is_created_by_system and __tmp3(
        created_on) or is_annotation_editable_for_user(user_id, created_on, annotation.user_id)


def is_annotation_editable_for_user(user_id, created_on, created_by_id):
    return user_id == created_by_id and __tmp3(created_on)


def __tmp3(created_on):
    global DELETION_EXPIRATION_THRESHOLD_IN_HOURS

    current_time = timezone.now()
    time_difference = current_time - created_on
    time_difference_in_hours = time_difference.total_seconds() / 3600

    return time_difference_in_hours <= DELETION_EXPIRATION_THRESHOLD_IN_HOURS


def __tmp4(__tmp2):
    if __tmp13(__tmp2):
        return __tmp2 in ['True', 'true']

    return None


def __tmp1(__tmp10):
    global GENDER_MALE
    global GENDER_FEMALE
    global GENDER_NOT_SURE

    global GENDER_STRING_FEMALE
    global GENDER_STRING_MALE

    if __tmp10 is not None and __tmp10.isdigit():
        return __tmp10

    if __tmp10 == GENDER_STRING_MALE:
        return GENDER_MALE

    if __tmp10 == GENDER_STRING_FEMALE:
        return GENDER_FEMALE

    return GENDER_NOT_SURE


def parse_age_parameter(__tmp15):
    global AGE_ADULT
    global AGE_CHILD
    global AGE_ELDERLY
    global AGE_NOT_SURE

    global AGE_STRING_CHILD
    global AGE_STRING_ADULT
    global AGE_STRING_ELDERLY

    if __tmp15 is not None and __tmp15.isdigit():
        return __tmp15

    if __tmp15 == AGE_STRING_CHILD:
        return AGE_CHILD

    if __tmp15 == AGE_STRING_ADULT:
        return AGE_ADULT

    if __tmp15 == AGE_STRING_ELDERLY:
        return AGE_ELDERLY

    return AGE_NOT_SURE


def parse_age_to_constant(__tmp15):
    global AGE_ADULT
    global AGE_CHILD
    global AGE_ELDERLY
    global AGE_NOT_SURE

    global AGE_STRING_ADULT
    global AGE_STRING_CHILD
    global AGE_STRING_ELDERLY
    global AGE_STRING_UNSURE

    if __tmp15 is None:
        return __tmp15

    if __tmp15 == AGE_CHILD:
        return AGE_STRING_CHILD

    if __tmp15 == AGE_ADULT:
        return AGE_STRING_ADULT

    if __tmp15 == AGE_ELDERLY:
        return AGE_STRING_ELDERLY

    return AGE_STRING_UNSURE


def __tmp14(__tmp10):
    global GENDER_MALE
    global GENDER_FEMALE
    global GENDER_NOT_SURE

    global GENDER_STRING_MALE
    global GENDER_STRING_FEMALE
    global GENDER_STRING_UNSURE

    if __tmp10 is None:
        return __tmp10

    if __tmp10 == GENDER_MALE:
        return GENDER_STRING_MALE

    if __tmp10 == GENDER_FEMALE:
        return GENDER_STRING_FEMALE

    return GENDER_STRING_UNSURE
