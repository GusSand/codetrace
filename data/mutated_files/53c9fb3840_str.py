from typing import TypeAlias
__typ0 : TypeAlias = "bool"
import logging
import traceback

import sublime
import sublime_plugin

from ..anaconda_lib._typing import Dict, Any
from ..anaconda_lib.helpers import is_python
from ..anaconda_lib.builder.python_builder import AnacondaSetPythonBuilder


class AnacondaSetPythonInterpreter(sublime_plugin.TextCommand):
    """Sets or modifies the Venv of the current project"""

    def __tmp4(__tmp0, __tmp3) :
        try:
            sublime.active_window().show_input_panel(
                "Python Path:", __tmp0.get_current_interpreter_path(),
                __tmp0.update_interpreter_settings, None, None
            )
        except Exception:
            logging.error(traceback.format_exc())

    def update_interpreter_settings(__tmp0, __tmp5: <FILL>) :
        """Updates the project and adds/modifies the Venv path"""
        project_data = __tmp0.get_project_data()

        # Check if have settings set in the project settings
        if project_data.get('settings', False):

            try:
                # Try to get the python_interpreter key
                project_data['settings'].get('python_interpreter', False)
            except AttributeError:
                # If this happens that mean your settings is a sting not a dict
                sublime.message_dialog(
                    'Ops your project settings is missed up'
                )
            else:
                # Set the path and save the project
                project_data['settings']['python_interpreter'] = __tmp5
                __tmp0.save_project_data(project_data)
        else:
            # This will excute if settings key is not in you project settings
            project_data.update(
                {
                    'settings': {'python_interpreter': __tmp5}
                }
            )
            __tmp0.save_project_data(project_data)
            AnacondaSetPythonBuilder().update_interpreter_build_system(
                __tmp5
            )

    def save_project_data(__tmp0, __tmp1: Dict[str, Any]) :
        """Saves the provided data to the project settings"""
        sublime.active_window().set_project_data(__tmp1)
        sublime.status_message("Python path is set successfuly")

    def get_project_data(__tmp0) :
        """Return the project data for the current window"""
        return sublime.active_window().project_data()

    def get_current_interpreter_path(__tmp0) :
        """Returns the current path from the settings if possible"""
        try:
            return __tmp0.get_project_data()['settings']['python_interpreter']
        except Exception:
            return ''

    def __tmp2(__tmp0) :
        """Check this plug in is enabled"""
        return is_python(__tmp0.view)
