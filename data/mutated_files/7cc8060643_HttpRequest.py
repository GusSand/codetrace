from typing import TypeAlias
__typ0 : TypeAlias = "AddDetectionAnnotation"
from django.http import HttpRequest

from ajapaik.ajapaik.models import Album, AlbumPhoto, Photo, Profile
from ajapaik.ajapaik_face_recognition.api import AddSubjectData
from ajapaik.ajapaik_face_recognition.domain.add_additional_subject_data import AddAdditionalSubjectData
from ajapaik.ajapaik_face_recognition.models import FaceRecognitionRectangle
from ajapaik.ajapaik_face_recognition.views import save_subject_object, add_person_rectangle
from ajapaik.ajapaik_object_recognition.domain.add_detection_annotation import AddDetectionAnnotation
from ajapaik.ajapaik_object_recognition.models import ObjectDetectionAnnotation
from ajapaik.ajapaik_object_recognition.object_annotation_utils import GENDER_NOT_SURE, AGE_NOT_SURE
from ajapaik.ajapaik_object_recognition.service.object_annotation.object_annotation_common_service import \
    get_saved_label


def __tmp4(add_detection_annotation, __tmp1):
    wiki_data_label_id = add_detection_annotation.wiki_data_label_id
    subject_id = add_detection_annotation.subject_id

    photo_id = add_detection_annotation.photo_id

    if wiki_data_label_id is None and add_detection_annotation.is_saving_object:
        raise Exception('Object ID has to be provided for object annotation adding')

    if wiki_data_label_id is not None and len(wiki_data_label_id) > 0:
        __tmp3(add_detection_annotation)
    else:
        photo = Photo.objects.get(pk=photo_id)
        __tmp5 = add_person_rectangle(__tmp1.POST.copy(), photo, __tmp1.user.id)

        add_subject_data(__tmp5, add_detection_annotation, __tmp1)

        if subject_id is not None and subject_id > 0:
            save_detected_face(__tmp5, subject_id, __tmp1.user.id, __tmp1.user.profile)


def save_detected_face(new_rectangle_id, __tmp2, user_id, __tmp0):
    new_rectangle = FaceRecognitionRectangle.objects.get(pk=new_rectangle_id)
    person_album = Album.objects.get(pk=__tmp2)
    if (person_album and not AlbumPhoto.objects.filter(photo=new_rectangle.photo, album=person_album).exists()):
        albumPhoto = AlbumPhoto(album=person_album, photo=new_rectangle.photo, type=AlbumPhoto.FACE_TAGGED,
                                profile=__tmp0)
        albumPhoto.save()
        person_album.set_calculated_fields()
        person_album.save()

    save_subject_object(person_album, new_rectangle, user_id, __tmp0)


def add_subject_data(__tmp5, add_detection_annotation: __typ0, __tmp1: <FILL>):
    is_gender_sent = add_detection_annotation.gender is not None and add_detection_annotation.gender < GENDER_NOT_SURE
    is_age_sent = add_detection_annotation.age_group is not None and add_detection_annotation.age_group < AGE_NOT_SURE

    if is_gender_sent or is_age_sent:
        add_additional_subject_data = AddAdditionalSubjectData(
            subject_rectangle_id=__tmp5,
            age=add_detection_annotation.age_group,
            gender=add_detection_annotation.gender
        )

        AddSubjectData.add_subject_data(add_additional_subject_data, __tmp1)


def __tmp3(add_detection_annotation: __typ0):
    saved_label = get_saved_label(add_detection_annotation.wiki_data_label_id)

    photo_id = add_detection_annotation.photo_id
    user_id = add_detection_annotation.user_id

    x1 = add_detection_annotation.x1
    x2 = add_detection_annotation.x2
    y1 = add_detection_annotation.y1
    y2 = add_detection_annotation.y2

    new_annotation = ObjectDetectionAnnotation()

    new_annotation.photo = Photo.objects.get(pk=photo_id)

    new_annotation.x1 = x1
    new_annotation.x2 = x2
    new_annotation.y1 = y1
    new_annotation.y2 = y2
    new_annotation.detected_object = saved_label
    new_annotation.is_manual_detection = True

    new_annotation.user = Profile.objects.get(pk=user_id)
    new_annotation.save()

    if new_annotation.photo.first_annotation is None:
        new_annotation.photo.first_annotation = new_annotation.created_on
    new_annotation.photo.latest_annotation = new_annotation.created_on
    new_annotation.photo.annotation_count += 1
    new_annotation.photo.light_save()
