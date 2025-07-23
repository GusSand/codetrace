from typing import TypeAlias
__typ0 : TypeAlias = "QueryDict"
from django.http import QueryDict

from ajapaik.ajapaik_object_recognition import object_annotation_utils
from ajapaik.ajapaik_object_recognition.domain.detection_rectangle import get_if_key_present
from ajapaik.ajapaik_object_recognition.object_annotation_utils import parse_age_parameter, parse_gender_parameter


class __typ1:
    def __tmp1(__tmp0, parameters, annotation_id: <FILL>, user_id: int):
        age_suggestion = get_if_key_present(parameters, 'ageGroup')
        gender_suggestion = get_if_key_present(parameters, 'gender')

        __tmp0.annotation_id = annotation_id

        __tmp0.new_subject_id = object_annotation_utils.parse_parameter(parameters['newSubjectId'])
        __tmp0.new_age_suggestion = age_suggestion is not None and parse_age_parameter(age_suggestion)
        __tmp0.new_gender_suggestion = gender_suggestion is not None and parse_gender_parameter(gender_suggestion)

        __tmp0.user_id = user_id
