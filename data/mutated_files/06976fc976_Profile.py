from typing import TypeAlias
__typ0 : TypeAlias = "ObjectDetectionAnnotation"
__typ1 : TypeAlias = "RemoveObjectAnnotationFeedback"
from ajapaik.ajapaik.models import Profile
from ajapaik.ajapaik_object_recognition.domain.add_object_detection_feedback import AddObjectDetectionFeedback
from ajapaik.ajapaik_object_recognition.domain.remove_object_annotation_feedback import RemoveObjectAnnotationFeedback
from ajapaik.ajapaik_object_recognition.models import ObjectAnnotationFeedback, ObjectDetectionAnnotation
from ajapaik.ajapaik_object_recognition.service.object_annotation import object_annotation_common_service


def __tmp2(
        feedback,
        __tmp1,
        user: <FILL>,
        annotation
):
    feedback.confirmation = __tmp1.is_confirmation
    feedback.user = user
    feedback.object_detection_annotation = annotation

    if __tmp1.alternative_wiki_data_label_id is not None and len(__tmp1.alternative_wiki_data_label_id) > 0:
        alternative_object_suggestion = object_annotation_common_service\
            .get_saved_label(__tmp1.alternative_wiki_data_label_id)
        feedback.alternative_object = alternative_object_suggestion
    else:
        feedback.alternative_object = None


def __tmp0(__tmp1):
    annotation_id = __tmp1.object_annotation_id

    annotation = __typ0.objects.get(pk=annotation_id)
    user = Profile.objects.get(pk=__tmp1.user_id)

    existing_feedback = __tmp3(annotation, user)

    if existing_feedback is not None:
        __tmp2(existing_feedback, __tmp1, user, annotation)
        existing_feedback.save()
    else:
        new_feedback = ObjectAnnotationFeedback()
        __tmp2(new_feedback, __tmp1, user, annotation)
        new_feedback.save()


def __tmp3(annotation, user: Profile):
    try:
        return ObjectAnnotationFeedback.objects.get(
            user_id=user.id,
            object_detection_annotation_id=annotation.id
        )
    except ObjectAnnotationFeedback.DoesNotExist:
        return None


def remove_feedback(remove_object_annotation_feedback):
    user_id = remove_object_annotation_feedback.user_id
    annotation_id = remove_object_annotation_feedback.annotation_id

    user = Profile.objects.get(pk=user_id)
    object_annotation = __typ0.objects.get(pk=annotation_id)

    existing_feedback = ObjectAnnotationFeedback.objects.get(user=user, object_detection_annotation=object_annotation)

    existing_feedback.delete()
