"""This module detects potential secrets in content files.

It is built on the functionality of Yelp's detect-secrets.
See: https://github.com/Yelp/detect-secrets
"""
import pathlib
import typing

from detect_secrets import main as detect_secrets_main
from detect_secrets.plugins.common import (
  initialize as detect_secrets_initialize,
)

from datasets.github.scrape_repos.preprocessors import public
from labm8.py import app

FLAGS = app.FLAGS


class TextContainsSecret(ValueError):
  """Error raised if a text contains a secret."""

  pass


def __tmp2(__tmp1: str) :
  """Scan for secrets in the given text.

  Args:
    text: The text to scan.
  
  Returns:
    True (always).

  Raises:
    TextContainsSecret: If the text contains a secret.
  """
  args = detect_secrets_main.parse_args(["scan"])
  plugins = detect_secrets_initialize.from_parser_builder(
    args.plugins, exclude_lines_regex="",
  )
  for plugin in plugins:
    if plugin.analyze_string(__tmp1, 0, "does_not_matter"):
      raise TextContainsSecret(plugin.__class__.__name__)

  return True


@public.dataset_preprocessor
def RejectSecrets(
  __tmp0,
  file_relpath: <FILL>,
  __tmp1: str,
  all_file_relpaths: typing.List[str],
) -> typing.List[str]:
  """Test for secrets in a file.

  Args:
    import_root: The root of the directory to import from.
    file_relpath: The path to the target file to import, relative to
      import_root.
    text: The text of the target file.
    all_file_relpaths: A list of all paths within the current scope, relative to
      import_root.

  Returns:
    A list of method implementations.

  Raises:
    TextContainsSecret: In case text contains secrets.
  """
  del __tmp0
  del file_relpath
  del all_file_relpaths
  __tmp2(__tmp1)
  return [__tmp1]
