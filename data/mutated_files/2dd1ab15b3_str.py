# Copyright 2021 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from pathlib import Path
from enum import Enum
import os
import uuid
import webbrowser

import cirq_web

# Resolve the path so the bundle file can be accessed properly
_DIST_PATH = Path(cirq_web.__file__).parents[1] / "cirq_ts" / "dist"


class Env(Enum):
    JUPYTER = 1
    COLAB = 2
    OTHER = 3


class __typ0(ABC):
    """Abstract class for all widgets."""

    def __tmp5(__tmp0):
        """Initializes a Widget.

        Gives a widget a unique ID.
        """
        # Generate a unique UUID for every instance of a Widget.
        # This helps with adding visualizations to scenes, etc.
        __tmp0.id = str(uuid.uuid1())

    @abstractmethod
    def get_client_code(__tmp0) :
        """Returns HTML code to render the widget."""
        raise NotImplementedError()

    @abstractmethod
    def get_widget_bundle_name(__tmp0) :
        """Returns the name of the Javascript library file for this widget."""
        raise NotImplementedError()

    def __tmp2(__tmp0):
        """Allows the object's html to be easily displayed in a notebook
        by using the display() method.
        """
        __tmp3 = __tmp0.get_client_code()
        return __tmp0._create_html_content(__tmp3)

    def __tmp1(
        __tmp0,
        output_directory: str = './',
        file_name: str = 'bloch_sphere.html',
        open_in_browser: bool = False,
    ) :
        """Generates a portable HTML file of the widget that
        can be run anywhere. Prints out the absolute path of the file to the console.

        Args:
            output_directory: the directory in which the output file will be
            generated. The default is the current directory ('./')

            file_name: the name of the output file. Default is 'bloch_sphere'

            open_in_browser: if True, opens the newly generated file automatically in the browser.

        Returns:
            The path of the HTML file in as a Path object.
        """
        __tmp3 = __tmp0.get_client_code()
        contents = __tmp0._create_html_content(__tmp3)
        path_of_html_file = os.path.join(output_directory, file_name)
        with open(path_of_html_file, 'w', encoding='utf-8') as f:
            f.write(contents)

        if open_in_browser:
            webbrowser.open(path_of_html_file, new=2)

        return path_of_html_file

    def _get_bundle_script(__tmp0):
        """Returns the bundle script of a widget"""
        __tmp4 = __tmp0.get_widget_bundle_name()
        return __tmp6(__tmp4)

    def _create_html_content(__tmp0, __tmp3: <FILL>) :
        div = f"""
        <meta charset="UTF-8">
        <div id="{__tmp0.id}"></div>
        """

        bundle_script = __tmp0._get_bundle_script()

        return div + bundle_script + __tmp3


def __tmp6(__tmp4) :
    """Dumps the contents of a particular bundle file into a script tag.

    Args:
        bundle_filename: the path to the bundle file

    Returns:
        The bundle file as string (readable by browser) wrapped in HTML script tags.
    """
    bundle_file_path = os.path.join(_DIST_PATH, __tmp4)
    bundle_file = open(bundle_file_path, 'r', encoding='utf-8')
    bundle_file_contents = bundle_file.read()
    bundle_file.close()
    bundle_html = f'<script>{bundle_file_contents}</script>'

    return bundle_html
