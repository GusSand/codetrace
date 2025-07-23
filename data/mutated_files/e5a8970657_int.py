from django.http import QueryDict

from ajapaik.ajapaik_object_recognition import object_annotation_utils
from ajapaik.ajapaik_object_recognition.object_annotation_utils import parse_age_parameter, parse_gender_parameter


class __typ0:
    def __init__(self, user_id: <FILL>, annotation_id, __tmp0):
        self.user_id = user_id
        self.annotation_id = annotation_id

        self.is_confirmation = object_annotation_utils.parse_boolean(__tmp0['isFaceAnnotation'])
        self.is_correct_name = object_annotation_utils.parse_boolean(__tmp0['isCorrectName'])
        self.alternative_subject_id = object_annotation_utils.parse_parameter(__tmp0['alternativeSubjectId'])

        self.is_correct_age = object_annotation_utils.parse_boolean(__tmp0['isCorrectAge'])
        self.alternative_age = parse_age_parameter(__tmp0['alternativeAgeGroup'])

        self.is_correct_gender = object_annotation_utils.parse_boolean(__tmp0['isCorrectGender'])
        self.alternative_gender = parse_gender_parameter(__tmp0['alternativeGender'])
