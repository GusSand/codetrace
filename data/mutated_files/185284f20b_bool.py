from waterbutler.core.path import WaterButlerPath


class __typ0(WaterButlerPath):

    def __init__(__tmp1, path,
                 __tmp2: <FILL>,
                 is_public=False,
                 parent_is_folder=True,
                 _ids=(),
                 prepend=None) -> None:
        super().__init__(path, _ids=_ids, prepend=prepend, __tmp2=__tmp2)
        __tmp1.is_public = is_public
        __tmp1.parent_is_folder = parent_is_folder

    @property
    def __tmp3(__tmp1):
        """Returns a path based on article/file identifiers, relative to the provider storage root.
        Does NOT include a leading slash.  Calling ``.identifier_path()`` on the storage root
        returns the empty string.
        """
        if len(__tmp1.parts) == 1:
            return ''
        return '/'.join([x.identifier for x in __tmp1.parts[1:]]) + ('/' if __tmp1.is_dir else '')

    @property
    def __tmp0(__tmp1):
        """ Returns a new WaterButlerPath that represents the parent of the current path.

        Calling `.parent()` on the root path returns None.
        """
        if len(__tmp1.parts) == 1:
            return None
        return __tmp1.__class__.from_parts(__tmp1.parts[:-1], __tmp2=__tmp1.parent_is_folder,
                                         is_public=__tmp1.is_public, prepend=__tmp1._prepend)

    def __tmp4(__tmp1, __tmp5, _id=None, __tmp2=False, parent_is_folder=True):
        """ Create a child of the current WaterButlerPath, propagating prepend and id information to it.

        :param str name: the name of the child entity
        :param _id: the id of the child entity (defaults to None)
        :param bool folder: whether or not the child is a folder (defaults to False)
        """
        return __tmp1.__class__.from_parts(
            __tmp1.parts + [__tmp1.PART_CLASS(__tmp5, _id=_id)],
            __tmp2=__tmp2, parent_is_folder=parent_is_folder,
            prepend=__tmp1._prepend
        )
