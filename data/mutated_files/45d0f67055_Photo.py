from typing import TypeAlias
__typ0 : TypeAlias = "Command"
import datetime
from json import dumps

import face_recognition
from django.core.management.base import BaseCommand

from ajapaik.ajapaik.models import Photo
from ajapaik.ajapaik_face_recognition.models import FaceRecognitionRectangle


def __tmp0(__tmp1: <FILL>) :
    print('Processing photo %s' % __tmp1.pk)
    if __tmp1.width > 5000 or __tmp1.height > 5000:
        print('Skipping too big photo %s' % __tmp1.pk)
        return
    try:
        image = face_recognition.load_image_file(__tmp1.image)
    except:  # noqa
        return
    try:
        detected_faces = face_recognition.face_locations(image)
    except:  # noqa
        return
    for detected_face in detected_faces:
        new_rectangle = FaceRecognitionRectangle(
            __tmp1=__tmp1,
            coordinates=dumps(detected_face)
        )
        new_rectangle.save()
    __tmp1.face_detection_attempted_at = datetime.datetime.now()
    __tmp1.light_save()


class __typ0(BaseCommand):
    help = 'Will run face detection on all photos in our database that haven\'t had it run yet'

    def handle(self, *args, **options):
        photos = Photo.objects.filter(rephoto_of__isnull=True, back_of__isnull=True,
                                      face_detection_attempted_at__isnull=True).all()
        print('Found %s photos to run on' % photos.count())
        for __tmp1 in photos:
            __tmp0(__tmp1)
