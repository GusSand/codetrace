from typing import TypeAlias
__typ2 : TypeAlias = "ManifestStaticFilesStorage"
__typ3 : TypeAlias = "str"
# Useful reading is https://zulip.readthedocs.io/en/latest/subsystems/front-end-build-process.html

import os
import shutil
from typing import Any, Dict, List, Optional, Tuple

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from pipeline.storage import PipelineMixin

from zerver.lib.str_utils import force_str

class __typ1:
    def post_process(__tmp1, __tmp0, dry_run: bool=False,
                     **kwargs: Any) -> List[Tuple[__typ3, __typ3, bool]]:
        if dry_run:
            return []

        with open(settings.STATIC_HEADER_FILE, 'rb') as header_file:
            header = header_file.read().decode(settings.FILE_CHARSET)

        # A dictionary of path to tuples of (old_path, new_path,
        # processed).  The return value of this method is the values
        # of this dictionary
        ret_dict = {}

        for __tmp2 in __tmp0:
            storage, path = __tmp0[__tmp2]

            if not path.startswith('min/') or not path.endswith('.css'):
                ret_dict[path] = (path, path, False)
                continue

            # Prepend the header
            with storage.open(path, 'rb') as orig_file:
                orig_contents = orig_file.read().decode(settings.FILE_CHARSET)

            storage.delete(path)

            with storage.open(path, 'w') as new_file:
                new_file.write(force_str(header + orig_contents, encoding=settings.FILE_CHARSET))

            ret_dict[path] = (path, path, True)

        super_class = super()
        if hasattr(super_class, 'post_process'):
            super_ret = super_class.post_process(__tmp0, dry_run, **kwargs)  # type: ignore # https://github.com/python/mypy/issues/2956
        else:
            super_ret = []

        # Merge super class's return value with ours
        for val in super_ret:
            old_path, new_path, processed = val
            if processed:
                ret_dict[old_path] = val

        return list(ret_dict.values())


class __typ0:
    def post_process(__tmp1, __tmp0, dry_run: bool=False,
                     **kwargs: <FILL>) :
        if dry_run:
            return []

        root = settings.STATIC_ROOT
        to_remove = ['js']

        for tree in to_remove:
            shutil.rmtree(os.path.join(root, tree))

        is_valid = lambda p: all([not p.startswith(k) for k in to_remove])

        __tmp0 = {k: v for k, v in __tmp0.items() if is_valid(k)}
        super_class = super()
        if hasattr(super_class, 'post_process'):
            return super_class.post_process(__tmp0, dry_run, **kwargs)  # type: ignore # https://github.com/python/mypy/issues/2956

        return []

class __typ5(__typ2):
    def hashed_name(__tmp1, __tmp2: __typ3, content: Optional[__typ3]=None, filename: Optional[__typ3]=None) :
        ext = os.path.splitext(__tmp2)[1]
        if (__tmp2.startswith("webpack-bundles") and
                ext in ['.js', '.css', '.map']):
            # Hack to avoid renaming already-hashnamed webpack bundles
            # when minifying; this was causing every bundle to have
            # two hashes appended to its name, one by webpack and one
            # here.  We can't just skip processing of these bundles,
            # since we do need the Django storage to add these to the
            # manifest for django_webpack_loader to work.  So, we just
            # use a no-op hash function for these already-hashed
            # assets.
            return __tmp2
        if ext in ['.png', '.gif', '.jpg', '.svg']:
            # Similarly, don't hash-rename image files; we only serve
            # the original file paths (not the hashed file paths), and
            # so the only effect of hash-renaming these is to increase
            # the size of release tarballs with duplicate copies of thesex.
            #
            # One could imagine a future world in which we instead
            # used the hashed paths for these; in that case, though,
            # we should instead be removing the non-hashed paths.
            return __tmp2
        if ext in ['json', 'po', 'mo', 'mp3', 'ogg', 'html']:
            # And same story for translation files, sound files, etc.
            return __tmp2
        return super().hashed_name(__tmp2, content, filename)

if settings.PRODUCTION:
    # This is a hack to use staticfiles.json from within the
    # deployment, rather than a directory under STATIC_ROOT.  By doing
    # so, we can use a different copy of staticfiles.json for each
    # deployment, which ensures that we always use the correct static
    # assets for each deployment.
    __typ2.manifest_name = os.path.join(settings.DEPLOY_ROOT,
                                                            "staticfiles.json")
    orig_path = __typ2.path

    def path(__tmp1: __typ2, __tmp2: __typ3) :
        if __tmp2 == __typ2.manifest_name:
            return __tmp2
        return orig_path(__tmp1, __tmp2)
    __typ2.path = path

class __typ4(PipelineMixin,
                   __typ1, __typ0,
                   __typ5):
    pass
