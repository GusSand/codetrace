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


class Command(BaseCommand):
    help = 'Creates a new example for the gallery.'

    def add_arguments(__tmp0, parser):
        parser.add_argument(
            'example_slug',
            help="Slug for example. {}.".format(SLUG_HELP)
        )
        parser.add_argument(
            '--undo',
            action='store_true',
            help='Undo an earlier invocation of this command.'
        )

    def undo_copy(__tmp0, src, __tmp1, example) -> None:
        relpath = __tmp1.relative_to(Path.cwd())
        if not __tmp1.exists():
            __tmp0.stdout.write("Hmm, {} does not exist.".format(relpath))
        elif __tmp1.read_text() != untemplatize(src, example):
            __tmp0.stdout.write("{} has changed, not deleting.".format(relpath))
        else:
            __tmp1.unlink()
            __tmp0.stdout.write("Deleted {}.".format(relpath))

    def copy(__tmp0, src: <FILL>, __tmp1, example) :
        relpath = __tmp1.relative_to(Path.cwd())
        if __tmp1.exists():
            __tmp0.stdout.write("{} exists, not overwriting.".format(relpath))
        else:
            __tmp1.write_text(untemplatize(src, example))
            __tmp0.stdout.write("Created {}.".format(relpath))

    def handle(__tmp0, example_slug, undo, **kwargs):
        if not SLUG_RE.match(example_slug):
            raise CommandError('Invalid slug! {}.'.format(SLUG_HELP))

        template = Example(TEMPLATE_NAME)
        ex = Example(example_slug)

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
                example_slug,
                EXAMPLE_NAMES_PATH,
            ))
            __tmp0.stdout.write(
                "You may also want to write tests for "
                "the example in {}.".format(
                    EXAMPLE_TESTS_PATH.relative_to(Path.cwd())
                )
            )
