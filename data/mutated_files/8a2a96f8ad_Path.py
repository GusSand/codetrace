from typing import TypeAlias
__typ1 : TypeAlias = "Example"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "Command"
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


def untemplatize(f, example):
    return f.read_text().replace(TEMPLATE_NAME, example.basename)


class __typ0(BaseCommand):
    help = 'Creates a new example for the gallery.'

    def add_arguments(__tmp0, __tmp3):
        __tmp3.add_argument(
            'example_slug',
            help="Slug for example. {}.".format(SLUG_HELP)
        )
        __tmp3.add_argument(
            '--undo',
            action='store_true',
            help='Undo an earlier invocation of this command.'
        )

    def undo_copy(__tmp0, __tmp2: <FILL>, dest: Path, example) -> None:
        relpath = dest.relative_to(Path.cwd())
        if not dest.exists():
            __tmp0.stdout.write("Hmm, {} does not exist.".format(relpath))
        elif dest.read_text() != untemplatize(__tmp2, example):
            __tmp0.stdout.write("{} has changed, not deleting.".format(relpath))
        else:
            dest.unlink()
            __tmp0.stdout.write("Deleted {}.".format(relpath))

    def copy(__tmp0, __tmp2, dest: Path, example) :
        relpath = dest.relative_to(Path.cwd())
        if dest.exists():
            __tmp0.stdout.write("{} exists, not overwriting.".format(relpath))
        else:
            dest.write_text(untemplatize(__tmp2, example))
            __tmp0.stdout.write("Created {}.".format(relpath))

    def __tmp1(__tmp0, __tmp4: str, undo, **kwargs):
        if not SLUG_RE.match(__tmp4):
            raise CommandError('Invalid slug! {}.'.format(SLUG_HELP))

        template = __typ1(TEMPLATE_NAME)
        ex = __typ1(__tmp4)

        if undo:
            __tmp0.undo_copy(template.template_path, ex.template_path, ex)
            __tmp0.undo_copy(template.jinja2_path, ex.jinja2_path, ex)
            __tmp0.undo_copy(template.python_path, ex.python_path, ex)
        else:
            __tmp0.copy(template.template_path, ex.template_path, ex)
            __tmp0.copy(template.jinja2_path, ex.jinja2_path, ex)
            __tmp0.copy(template.python_path, ex.python_path, ex)

            __tmp0.stdout.write("\nDone! Now edit the above files.")
            __tmp0.stdout.write("Then, add '{}' to {}.".format(
                __tmp4,
                EXAMPLE_NAMES_PATH,
            ))
            __tmp0.stdout.write(
                "You may also want to write tests for "
                "the example in {}.".format(
                    EXAMPLE_TESTS_PATH.relative_to(Path.cwd())
                )
            )
