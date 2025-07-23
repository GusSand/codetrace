from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ2 : TypeAlias = "Example"
__typ0 : TypeAlias = "str"
__typ3 : TypeAlias = "bool"
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


def untemplatize(f, example: __typ2):
    return f.read_text().replace(TEMPLATE_NAME, example.basename)


class Command(BaseCommand):
    help = 'Creates a new example for the gallery.'

    def __tmp0(__tmp1, parser):
        parser.add_argument(
            'example_slug',
            help="Slug for example. {}.".format(SLUG_HELP)
        )
        parser.add_argument(
            '--undo',
            action='store_true',
            help='Undo an earlier invocation of this command.'
        )

    def undo_copy(__tmp1, src: Path, dest, example: __typ2) :
        relpath = dest.relative_to(Path.cwd())
        if not dest.exists():
            __tmp1.stdout.write("Hmm, {} does not exist.".format(relpath))
        elif dest.read_text() != untemplatize(src, example):
            __tmp1.stdout.write("{} has changed, not deleting.".format(relpath))
        else:
            dest.unlink()
            __tmp1.stdout.write("Deleted {}.".format(relpath))

    def copy(__tmp1, src: Path, dest: <FILL>, example: __typ2) :
        relpath = dest.relative_to(Path.cwd())
        if dest.exists():
            __tmp1.stdout.write("{} exists, not overwriting.".format(relpath))
        else:
            dest.write_text(untemplatize(src, example))
            __tmp1.stdout.write("Created {}.".format(relpath))

    def handle(__tmp1, example_slug, undo, **kwargs):
        if not SLUG_RE.match(example_slug):
            raise CommandError('Invalid slug! {}.'.format(SLUG_HELP))

        template = __typ2(TEMPLATE_NAME)
        ex = __typ2(example_slug)

        if undo:
            __tmp1.undo_copy(template.template_path, ex.template_path, ex)
            __tmp1.undo_copy(template.jinja2_path, ex.jinja2_path, ex)
            __tmp1.undo_copy(template.python_path, ex.python_path, ex)
        else:
            __tmp1.copy(template.template_path, ex.template_path, ex)
            __tmp1.copy(template.jinja2_path, ex.jinja2_path, ex)
            __tmp1.copy(template.python_path, ex.python_path, ex)

            __tmp1.stdout.write("\nDone! Now edit the above files.")
            __tmp1.stdout.write("Then, add '{}' to {}.".format(
                example_slug,
                EXAMPLE_NAMES_PATH,
            ))
            __tmp1.stdout.write(
                "You may also want to write tests for "
                "the example in {}.".format(
                    EXAMPLE_TESTS_PATH.relative_to(Path.cwd())
                )
            )
