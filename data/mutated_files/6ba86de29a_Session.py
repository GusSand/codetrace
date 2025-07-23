from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "FaceVector"
__typ0 : TypeAlias = "float"
from datetime import datetime
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np
from sqlalchemy.orm import Session

from faceanalysis.face_vectorizer import face_vector_from_text, FaceVector
from faceanalysis.face_vectorizer import face_vector_to_text
from faceanalysis.face_vectorizer import get_face_vectors
from faceanalysis.log import get_logger
from faceanalysis.models import FeatureMapping
from faceanalysis.models import Image
from faceanalysis.models import ImageStatus
from faceanalysis.models import ImageStatusEnum
from faceanalysis.models import Match
from faceanalysis.models import get_db_session
from faceanalysis.settings import DISTANCE_SCORE_THRESHOLD
from faceanalysis.settings import FACE_VECTORIZE_ALGORITHM
from faceanalysis.storage import StorageError
from faceanalysis.storage import delete_image
from faceanalysis.storage import get_image_path

logger = get_logger(__name__)


def __tmp12(__tmp4, session: <FILL>, **kwargs):
    logger.debug('adding entry to session')
    row = __tmp4(**kwargs)
    session.add(row)
    return row


def __tmp0(features: __typ2, img_id, session):
    logger.debug('processing feature mapping')
    __tmp12(FeatureMapping, session,
                          img_id=img_id,
                          features=face_vector_to_text(features))
    return features


def __tmp6(__tmp1: __typ1,
                   __tmp11,
                   __tmp3,
                   session: Session):

    logger.debug('processing matches')
    __tmp12(Match, session,
                          __tmp1=__tmp1,
                          __tmp11=__tmp11,
                          __tmp3=__tmp3)
    __tmp12(Match, session,
                          __tmp1=__tmp11,
                          __tmp11=__tmp1,
                          __tmp3=__tmp3)


def __tmp7() :
    logger.debug('getting all img ids and respective features')

    with get_db_session() as session:
        rows = session.query(FeatureMapping)\
            .all()

    known_features = []
    img_ids = []
    for row in rows:
        img_ids.append(row.img_id)
        current_features = np.array(face_vector_from_text(row.features))
        known_features.append(current_features)
    return img_ids, np.array(known_features)


def __tmp9(__tmp13,
                     __tmp11: __typ1,
                     __tmp3: __typ0):

    match_exists = False
    for match in __tmp13:
        if match["that_img_id"] == __tmp11:
            match_exists = True
            match["distance_score"] = min(match["distance_score"],
                                          __tmp3)

    if not match_exists:
        __tmp13.append({
            "that_img_id": __tmp11,
            "distance_score": __tmp3
        })


def __tmp8(img_id,
                       status: Optional[ImageStatusEnum] = None,
                       error_msg: Optional[__typ1] = None):
    update_fields = {}
    if status:
        update_fields['status'] = status.name
    if error_msg:
        update_fields['error_msg'] = error_msg

    with get_db_session(commit=True) as session:
        session.query(ImageStatus)\
            .filter(ImageStatus.img_id == img_id)\
            .update(update_fields)


# pylint: disable=len-as-condition
def __tmp2(face_encodings: np.array,
                       __tmp10: __typ2) -> np.array:

    if len(face_encodings) == 0:
        return np.empty(0)

    __tmp10 = np.array(__tmp10)
    return np.linalg.norm(face_encodings - __tmp10, axis=1)
# pylint: enable=len-as-condition


def __tmp5(img_id: __typ1):
    logger.info('Processing image %s', img_id)
    try:
        img_path = get_image_path(img_id)
    except StorageError:
        logger.error("Can't process image %s since it doesn't exist", img_id)
        __tmp8(img_id, error_msg='Image processed before uploaded')
        return

    start = datetime.utcnow()
    __tmp8(img_id, status=ImageStatusEnum.processing)

    prev_img_ids, prev_face_vectors = __tmp7()
    face_vectors = get_face_vectors(img_path, FACE_VECTORIZE_ALGORITHM)
    logger.info('Found %d faces in image %s', len(face_vectors), img_id)
    __tmp8(img_id, status=ImageStatusEnum.face_vector_computed)

    with get_db_session(commit=True) as session:
        __tmp12(Image, session, img_id=img_id)
        __tmp13 = []  # type: List[dict]
        for face_vector in face_vectors:
            __tmp0(face_vector, img_id, session)

            distances = __tmp2(prev_face_vectors, face_vector)
            for __tmp11, distance in zip(prev_img_ids, distances):
                if img_id == __tmp11:
                    continue
                distance = __typ0(distance)
                if distance >= DISTANCE_SCORE_THRESHOLD:
                    continue
                __tmp9(__tmp13, __tmp11, distance)

        logger.info('Found %d face matches for image %s', len(__tmp13), img_id)
        for match in __tmp13:
            __tmp6(img_id, match["that_img_id"],
                           match["distance_score"], session)

    __tmp8(img_id,
                       status=ImageStatusEnum.finished_processing,
                       error_msg=('No faces found in image'
                                  if not face_vectors else None))
    delete_image(img_id)

    processing_time = (datetime.utcnow() - start).total_seconds()
    logger.info('Processed image %s in %d seconds', img_id, processing_time)
