from typing import TypeAlias
__typ0 : TypeAlias = "FaceRecognitionRectangle"
__typ1 : TypeAlias = "HttpRequest"
__typ2 : TypeAlias = "FaceAnnotationFeedbackRequest"
from django.http import HttpRequest

from ajapaik.ajapaik.models import Profile, Album
from ajapaik.ajapaik_face_recognition.api import AddSubjectData
from ajapaik.ajapaik_face_recognition.domain.add_additional_subject_data import AddAdditionalSubjectData
from ajapaik.ajapaik_face_recognition.domain.face_annotation_feedback_request import FaceAnnotationFeedbackRequest
from ajapaik.ajapaik_face_recognition.models import FaceRecognitionRectangle, FaceRecognitionRectangleFeedback
from ajapaik.ajapaik_face_recognition.service.face_annotation_edit_service import \
    get_existing_user_additional_data_suggestion


def add_feedback(request, __tmp2):
    face_annotation = __typ0.objects.get(pk=request.annotation_id)
    user = Profile.objects.get(pk=request.user_id)

    # TODO: Some kind of review process to delete rectangles not liked by N people?
    existing_feedback = get_existing_feedback(face_annotation, user)

    if existing_feedback is not None:
        __tmp0(existing_feedback, request, user, face_annotation)
        existing_feedback.save()
        if face_annotation.photo.first_annotation is None:
            face_annotation.photo.first_annotation = existing_feedback.modified
        face_annotation.photo.latest_annotation = existing_feedback.modified
        face_annotation.photo.light_save()
    else:
        new_feedback = FaceRecognitionRectangleFeedback()
        __tmp0(new_feedback, request, user, face_annotation)
        new_feedback.save()
        if face_annotation.photo.first_annotation is None:
            face_annotation.photo.first_annotation = new_feedback.modified
        face_annotation.photo.latest_annotation = new_feedback.modified
        face_annotation.photo.light_save()

    if not request.is_correct_age or not request.is_correct_gender:
        __tmp1(user, face_annotation, request, __tmp2)


def get_existing_feedback(annotation, user):
    try:
        return FaceRecognitionRectangleFeedback.objects.get(
            user_id=user.id,
            rectangle_id=annotation.id
        )
    except FaceRecognitionRectangleFeedback.DoesNotExist:
        return None


def __tmp0(
        feedback,
        request,
        user: <FILL>,
        annotation
):
    feedback.is_correct = request.is_confirmation
    feedback.user = user
    feedback.rectangle = annotation

    if request.is_correct_name is not None:
        feedback.is_correct_person = request.is_correct_name

    if request.alternative_subject_id is not None and request.alternative_subject_id > 0:
        alternative_subject_suggestion = Album.objects.get(pk=request.alternative_subject_id)
        feedback.alternative_subject = alternative_subject_suggestion
    else:
        feedback.alternative_subject = None


def __tmp1(
        user,
        face_annotation,
        request,
        __tmp2: __typ1
):
    existing_additional_data_suggestion = get_existing_user_additional_data_suggestion(user, face_annotation.id)

    age = None if request.is_correct_age else request.alternative_age
    gender = None if request.is_correct_gender else request.alternative_gender

    if existing_additional_data_suggestion is None:
        add_additional_subject_data = AddAdditionalSubjectData(
            subject_rectangle_id=face_annotation.id,
            age=age,
            gender=gender
        )
        AddSubjectData.add_subject_data(add_additional_subject_data, __tmp2)
    else:
        existing_additional_data_suggestion.age = age
        existing_additional_data_suggestion.gender = gender
        existing_additional_data_suggestion.save()
