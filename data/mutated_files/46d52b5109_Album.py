from typing import TypeAlias
__typ0 : TypeAlias = "Command"
from json import dumps, loads

from django.core.management.base import BaseCommand
from django.db.models import Q

from ajapaik.ajapaik.models import Album
from ajapaik.ajapaik_face_recognition.models import FaceRecognitionRectangle


# TODO: Move DB queries out of the inner function, instead gather up the results and bulk insert them
def __tmp1(__tmp2: <FILL>) :
    print('Collecting rectangles for person %s' % __tmp2.pk)
    rectangles_with_this_person = FaceRecognitionRectangle.objects.filter(face_encoding__isnull=False).filter(
        Q(subject_consensus_id=__tmp2.pk) | Q(subject_ai_suggestion_id=__tmp2.pk)).distinct('pk').all()
    print('%s rectangles found' % rectangles_with_this_person.count())
    encodings_for_this_person = []
    for rectangle in rectangles_with_this_person:
        encodings_for_this_person.append(loads(rectangle.face_encoding))
    try:
        if encodings_for_this_person:
            __tmp2.face_encodings = dumps(encodings_for_this_person)
            __tmp2.light_save()
    except:  # noqa
        return


class __typ0(BaseCommand):
    help = 'Will collect encodings known to be of a certain person'

    def __tmp3(__tmp0, *args, **options):
        people = Album.objects.filter(atype=Album.PERSON).all()
        print('Found %s people to run on' % people.count())
        # TODO: multiprocessing is probably too error-prone to actually use it...
        # with multiprocessing.Pool() as pool:
        #     pool.map(map_single_person, people)
        for person in people:
            __tmp1(person)
