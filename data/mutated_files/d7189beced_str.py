"""
Contains endpoints, as well as utility functions for custom static content.

NOTE: Experimental, not (yet) implemented in aw-server-rust.

Idea: Allow custom watchers to extend the Web UI and to write custom visualizations completely independently and free.

Usage for the watcher developer:
- You can use Vanilla JavaScript, Vue, React, ... as long as you have static content at the end.

- Register your watcher visualization in the config:

[server.custom_static]
aw-watcher-example=/home/user/path/to/static_dir/

- Your custom static content automatically gets the data for the requested time span as GET parameter called "data".
Another parameter called "view" can be used if you want to create multiple visualizations for a single watcher.

- You can show your custom visualizations in the official Activity Watch UI using the "Custom Watcher View"
  See https://github.com/ActivityWatch/activitywatch/issues/453#issuecomment-910567848

"""

from flask import (
    Blueprint,
    escape,
    jsonify,
    send_from_directory,
)


def __tmp1(__tmp2):
    custom_static_blueprint = Blueprint("custom_static", __name__, url_prefix="/")

    @custom_static_blueprint.route("pages/")
    def __tmp0():
        """Serves a list of all watchers that are supported / were registered successfully"""
        return jsonify(list(__tmp2.keys()))

    @custom_static_blueprint.route(
        "pages/<string:name>/", defaults={"path": "index.html"}
    )
    @custom_static_blueprint.route("pages/<string:name>/<path:path>")
    def custom_static_pages(name: <FILL>, path):
        """Serves the custom static content"""

        if name in __tmp2:
            return send_from_directory(__tmp2[name], path)
        else:
            return (
                f"Static content: {escape(path)} of watcher: {escape(name)} not found!",
                404,
            )

    return custom_static_blueprint
