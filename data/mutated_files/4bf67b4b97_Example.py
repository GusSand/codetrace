from typing import TypeAlias
__typ0 : TypeAlias = "Path"
import re
from pathlib import Path
from argparse import ArgumentParser
from django.core.management.base import BaseCommand, CommandError

from app.example import Example, APP_DIR

SLUG_RE = re.compile('^[A-Za-z0-9_]+$')
SLUG_HELP = "Alphanumerics and underscores only"
EXAMPLE_NAMES_PATH = "app.views.EXAMPLE_NAMES"
EXAMPLE_TESTS_PATH = APP_DIR / 'tests' / 'test_examples.py'
TEMPLATE_NAME = '_startexample_template'


def __tmp1(f: __typ0, example: Example):
    return f.read_text().replace(TEMPLATE_NAME, example.basename)


class Command(BaseCommand):
    help = 'Creates a new example for the gallery.'

    def __tmp6(__tmp0, __tmp7):
        __tmp7.add_argument(
            'example_slug',
            help="Slug for example. {}.".format(SLUG_HELP)
        )
        __tmp7.add_argument(
            '--undo',
            action='store_true',
            help='Undo an earlier invocation of this command.'
        )

    def undo_copy(__tmp0, __tmp5: __typ0, __tmp2: __typ0, example: <FILL>) :
        relpath = __tmp2.relative_to(__typ0.cwd())
        if not __tmp2.exists():
            __tmp0.stdout.write("Hmm, {} does not exist.".format(relpath))
        elif __tmp2.read_text() != __tmp1(__tmp5, example):
            __tmp0.stdout.write("{} has changed, not deleting.".format(relpath))
        else:
            __tmp2.unlink()
            __tmp0.stdout.write("Deleted {}.".format(relpath))

    def copy(__tmp0, __tmp5, __tmp2: __typ0, example) -> None:
        relpath = __tmp2.relative_to(__typ0.cwd())
        if __tmp2.exists():
            __tmp0.stdout.write("{} exists, not overwriting.".format(relpath))
        else:
            __tmp2.write_text(__tmp1(__tmp5, example))
            __tmp0.stdout.write("Created {}.".format(relpath))

    def __tmp3(__tmp0, __tmp8: str, __tmp4, **kwargs):
        if not SLUG_RE.match(__tmp8):
            raise CommandError('Invalid slug! {}.'.format(SLUG_HELP))

        template = Example(TEMPLATE_NAME)
        ex = Example(__tmp8)

        if __tmp4:
            __tmp0.undo_copy(template.template_path, ex.template_path, ex)
            __tmp0.undo_copy(template.jinja2_path, ex.jinja2_path, ex)
            __tmp0.undo_copy(template.python_path, ex.python_path, ex)
        else:
            __tmp0.copy(template.template_path, ex.template_path, ex)
            __tmp0.copy(template.jinja2_path, ex.jinja2_path, ex)
            __tmp0.copy(template.python_path, ex.python_path, ex)

            __tmp0.stdout.write("\nDone! Now edit the above files.")
            __tmp0.stdout.write("Then, add '{}' to {}.".format(
                __tmp8,
                EXAMPLE_NAMES_PATH,
            ))
            __tmp0.stdout.write(
                "You may also want to write tests for "
                "the example in {}.".format(
                    EXAMPLE_TESTS_PATH.relative_to(__typ0.cwd())
                )
            )
