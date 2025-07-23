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


def __tmp13(__tmp18):
    return __tmp18 is not None and len(__tmp18) > 0


def __tmp20(__tmp21):
    if __tmp13(__tmp21):
        return int(__tmp21)

    return 0


def __tmp3(__tmp5):
    query_dictionary = QueryDict('', mutable=True)
    query_dictionary.update(__tmp5)
    return query_dictionary


def __tmp19(user_id, __tmp12, __tmp22, photo_id=None):
    transformed_collection = []

    for entry in __tmp12:
        transformed_collection.append(json.dumps(__tmp22(entry, user_id).__dict__))
    return transformed_collection


def __tmp23(user_id: <FILL>, __tmp0):
    created_on = __tmp0.created_on
    __tmp4 = __tmp0.user_id

    return __tmp6(user_id, created_on, __tmp4)


def __tmp2(user_id, __tmp11):
    created_on = __tmp11.created
    created_by = __tmp11.user

    is_without_name = __tmp11.get_subject_name() is None
    is_created_by_system = created_by is None

    return is_without_name or is_created_by_system and __tmp9(
        created_on) or __tmp6(user_id, created_on, __tmp11.user_id)


def __tmp6(user_id, created_on, __tmp4):
    return user_id == __tmp4 and __tmp9(created_on)


def __tmp9(created_on):
    global DELETION_EXPIRATION_THRESHOLD_IN_HOURS

    current_time = timezone.now()
    time_difference = current_time - created_on
    time_difference_in_hours = time_difference.total_seconds() / 3600

    return time_difference_in_hours <= DELETION_EXPIRATION_THRESHOLD_IN_HOURS


def __tmp15(__tmp14):
    if __tmp13(__tmp14):
        return __tmp14 in ['True', 'true']

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


def __tmp7(__tmp8):
    global AGE_ADULT
    global AGE_CHILD
    global AGE_ELDERLY
    global AGE_NOT_SURE

    global AGE_STRING_CHILD
    global AGE_STRING_ADULT
    global AGE_STRING_ELDERLY

    if __tmp8 is not None and __tmp8.isdigit():
        return __tmp8

    if __tmp8 == AGE_STRING_CHILD:
        return AGE_CHILD

    if __tmp8 == AGE_STRING_ADULT:
        return AGE_ADULT

    if __tmp8 == AGE_STRING_ELDERLY:
        return AGE_ELDERLY

    return AGE_NOT_SURE


def __tmp16(__tmp8):
    global AGE_ADULT
    global AGE_CHILD
    global AGE_ELDERLY
    global AGE_NOT_SURE

    global AGE_STRING_ADULT
    global AGE_STRING_CHILD
    global AGE_STRING_ELDERLY
    global AGE_STRING_UNSURE

    if __tmp8 is None:
        return __tmp8

    if __tmp8 == AGE_CHILD:
        return AGE_STRING_CHILD

    if __tmp8 == AGE_ADULT:
        return AGE_STRING_ADULT

    if __tmp8 == AGE_ELDERLY:
        return AGE_STRING_ELDERLY

    return AGE_STRING_UNSURE


def __tmp17(__tmp10):
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
