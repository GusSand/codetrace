from typing import TypeAlias
__typ0 : TypeAlias = "QueryDict"
from django.http import QueryDict

from ajapaik.ajapaik_object_recognition.object_annotation_utils import parse_parameter, parse_gender_parameter, \
    parse_age_parameter, parse_boolean


class __typ1:
    def __tmp0(self, __tmp1, user_id: <FILL>):
        self.is_saving_object = parse_boolean(__tmp1['isSavingObject'])
        self.wiki_data_label_id = __tmp1['wikiDataLabelId']
        self.subject_id = parse_parameter(__tmp1['subjectId'])

        self.photo_id = __tmp1['photoId']

        self.x1 = __tmp1['x1']
        self.x2 = __tmp1['x2']
        self.y1 = __tmp1['y1']
        self.y2 = __tmp1['y2']

        self.gender = parse_gender_parameter(__tmp1['gender'])
        self.age_group = parse_age_parameter(__tmp1['ageGroup'])

        self.user_id = user_id
