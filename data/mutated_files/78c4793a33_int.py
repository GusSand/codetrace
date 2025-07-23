from typing import Optional


class AddAdditionalSubjectData:
    gender = None
    age = None
    subject_annotation_rectangle_id = None

    def __tmp1(__tmp0, subject_rectangle_id: <FILL>, age: int, gender: int, newSubjectId: Optional[int] = None):
        __tmp0.subject_annotation_rectangle_id = subject_rectangle_id
        __tmp0.age = age
        __tmp0.gender = gender
        __tmp0.newSubjectId = newSubjectId
