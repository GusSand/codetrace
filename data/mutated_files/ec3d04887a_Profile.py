from typing import TypeAlias
__typ1 : TypeAlias = "ObjectDetectionAnnotation"
__typ2 : TypeAlias = "ObjectAnnotationFeedback"
__typ0 : TypeAlias = "AddObjectDetectionFeedback"
from ajapaik.ajapaik.models import Profile
from ajapaik.ajapaik_object_recognition.domain.add_object_detection_feedback import AddObjectDetectionFeedback
from ajapaik.ajapaik_object_recognition.domain.remove_object_annotation_feedback import RemoveObjectAnnotationFeedback
from ajapaik.ajapaik_object_recognition.models import ObjectAnnotationFeedback, ObjectDetectionAnnotation
from ajapaik.ajapaik_object_recognition.service.object_annotation import object_annotation_common_service


def set_feedback(
        feedback,
        __tmp0,
        user: Profile,
        annotation
):
    feedback.confirmation = __tmp0.is_confirmation
    feedback.user = user
    feedback.object_detection_annotation = annotation

    if __tmp0.alternative_wiki_data_label_id is not None and len(__tmp0.alternative_wiki_data_label_id) > 0:
        alternative_object_suggestion = object_annotation_common_service\
            .get_saved_label(__tmp0.alternative_wiki_data_label_id)
        feedback.alternative_object = alternative_object_suggestion
    else:
        feedback.alternative_object = None


def add_feedback(__tmp0):
    annotation_id = __tmp0.object_annotation_id

    annotation = __typ1.objects.get(pk=annotation_id)
    user = Profile.objects.get(pk=__tmp0.user_id)

    existing_feedback = __tmp1(annotation, user)

    if existing_feedback is not None:
        set_feedback(existing_feedback, __tmp0, user, annotation)
        existing_feedback.save()
    else:
        new_feedback = __typ2()
        set_feedback(new_feedback, __tmp0, user, annotation)
        new_feedback.save()


def __tmp1(annotation, user: <FILL>):
    try:
        return __typ2.objects.get(
            user_id=user.id,
            object_detection_annotation_id=annotation.id
        )
    except __typ2.DoesNotExist:
        return None


def __tmp2(remove_object_annotation_feedback):
    user_id = remove_object_annotation_feedback.user_id
    annotation_id = remove_object_annotation_feedback.annotation_id

    user = Profile.objects.get(pk=user_id)
    object_annotation = __typ1.objects.get(pk=annotation_id)

    existing_feedback = __typ2.objects.get(user=user, object_detection_annotation=object_annotation)

    existing_feedback.delete()
