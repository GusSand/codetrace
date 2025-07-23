from typing import TypeAlias
__typ1 : TypeAlias = "QueryDict"
from django.http import QueryDict

from ajapaik.ajapaik_object_recognition import object_annotation_utils


class __typ0:
    def __tmp1(__tmp0, __tmp2, user_id: <FILL>, annotation_id):
        __tmp0.user_id = user_id

        __tmp0.object_annotation_id = object_annotation_utils.parse_parameter(annotation_id)
        __tmp0.is_confirmation = object_annotation_utils.parse_boolean(__tmp2['isConfirmed'])
        __tmp0.alternative_wiki_data_label_id = __tmp2['alternativeWikiDataLabelId']
