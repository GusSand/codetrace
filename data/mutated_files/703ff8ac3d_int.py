from django.http import QueryDict

from ajapaik.ajapaik_object_recognition import object_annotation_utils
from ajapaik.ajapaik_object_recognition.object_annotation_utils import parse_age_parameter, parse_gender_parameter


class FaceAnnotationFeedbackRequest:
    def __tmp1(__tmp0, user_id, annotation_id: <FILL>, __tmp2):
        __tmp0.user_id = user_id
        __tmp0.annotation_id = annotation_id

        __tmp0.is_confirmation = object_annotation_utils.parse_boolean(__tmp2['isFaceAnnotation'])
        __tmp0.is_correct_name = object_annotation_utils.parse_boolean(__tmp2['isCorrectName'])
        __tmp0.alternative_subject_id = object_annotation_utils.parse_parameter(__tmp2['alternativeSubjectId'])

        __tmp0.is_correct_age = object_annotation_utils.parse_boolean(__tmp2['isCorrectAge'])
        __tmp0.alternative_age = parse_age_parameter(__tmp2['alternativeAgeGroup'])

        __tmp0.is_correct_gender = object_annotation_utils.parse_boolean(__tmp2['isCorrectGender'])
        __tmp0.alternative_gender = parse_gender_parameter(__tmp2['alternativeGender'])
