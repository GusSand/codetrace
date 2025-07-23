from typing import TypeAlias
__typ0 : TypeAlias = "Path"
__typ1 : TypeAlias = "bool"
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


def untemplatize(f: __typ0, example: <FILL>):
    return f.read_text().replace(TEMPLATE_NAME, example.basename)


class Command(BaseCommand):
    help = 'Creates a new example for the gallery.'

    def __tmp1(self, parser: ArgumentParser):
        parser.add_argument(
            'example_slug',
            help="Slug for example. {}.".format(SLUG_HELP)
        )
        parser.add_argument(
            '--undo',
            action='store_true',
            help='Undo an earlier invocation of this command.'
        )

    def undo_copy(self, __tmp0, __tmp3: __typ0, example) -> None:
        relpath = __tmp3.relative_to(__typ0.cwd())
        if not __tmp3.exists():
            self.stdout.write("Hmm, {} does not exist.".format(relpath))
        elif __tmp3.read_text() != untemplatize(__tmp0, example):
            self.stdout.write("{} has changed, not deleting.".format(relpath))
        else:
            __tmp3.unlink()
            self.stdout.write("Deleted {}.".format(relpath))

    def copy(self, __tmp0: __typ0, __tmp3: __typ0, example: Example) -> None:
        relpath = __tmp3.relative_to(__typ0.cwd())
        if __tmp3.exists():
            self.stdout.write("{} exists, not overwriting.".format(relpath))
        else:
            __tmp3.write_text(untemplatize(__tmp0, example))
            self.stdout.write("Created {}.".format(relpath))

    def handle(self, __tmp2, undo, **kwargs):
        if not SLUG_RE.match(__tmp2):
            raise CommandError('Invalid slug! {}.'.format(SLUG_HELP))

        template = Example(TEMPLATE_NAME)
        ex = Example(__tmp2)

        if undo:
            self.undo_copy(template.template_path, ex.template_path, ex)
            self.undo_copy(template.jinja2_path, ex.jinja2_path, ex)
            self.undo_copy(template.python_path, ex.python_path, ex)
        else:
            self.copy(template.template_path, ex.template_path, ex)
            self.copy(template.jinja2_path, ex.jinja2_path, ex)
            self.copy(template.python_path, ex.python_path, ex)

            self.stdout.write("\nDone! Now edit the above files.")
            self.stdout.write("Then, add '{}' to {}.".format(
                __tmp2,
                EXAMPLE_NAMES_PATH,
            ))
            self.stdout.write(
                "You may also want to write tests for "
                "the example in {}.".format(
                    EXAMPLE_TESTS_PATH.relative_to(__typ0.cwd())
                )
            )
