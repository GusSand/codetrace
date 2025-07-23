from typing import TypeAlias
__typ1 : TypeAlias = "bool"
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List

import aw_datastore
import flask.json.provider
from aw_datastore import Datastore
from flask import (
    Blueprint,
    Flask,
    current_app,
    send_from_directory,
)
from flask_cors import CORS

from . import rest
from .api import ServerAPI
from .custom_static import get_custom_static_blueprint
from .log import FlaskLogHandler

logger = logging.getLogger(__name__)

app_folder = os.path.dirname(os.path.abspath(__file__))
static_folder = os.path.join(app_folder, "static")

root = Blueprint("root", __name__, url_prefix="/")


class __typ2(Flask):
    def __init__(
        __tmp0,
        host,
        testing: __typ1,
        __tmp1=None,
        cors_origins=[],
        custom_static=dict(),
        static_folder=static_folder,
        static_url_path="",
    ):
        name = "aw-server"
        __tmp0.json_provider_class = __typ0
        # only prettyprint JSON if testing (due to perf)
        __tmp0.json_provider_class.compact = not testing

        # Initialize Flask
        Flask.__init__(
            __tmp0,
            name,
            static_folder=static_folder,
            static_url_path=static_url_path,
        )
        __tmp0.config["HOST"] = host  # needed for host-header check
        with __tmp0.app_context():
            _config_cors(cors_origins, testing)

        # Initialize datastore and API
        if __tmp1 is None:
            __tmp1 = aw_datastore.get_storage_methods()["memory"]
        db = Datastore(__tmp1, testing=testing)
        __tmp0.api = ServerAPI(db=db, testing=testing)

        __tmp0.register_blueprint(root)
        __tmp0.register_blueprint(rest.blueprint)
        __tmp0.register_blueprint(get_custom_static_blueprint(custom_static))


class __typ0(flask.json.provider.DefaultJSONProvider):
    # encoding/decoding of datetime as iso8601 strings
    # encoding of timedelta as second floats
    def default(__tmp0, obj, *args, **kwargs):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, timedelta):
                return obj.total_seconds()
        except TypeError:
            pass
        return super().default(obj)


@root.route("/")
def __tmp2():
    return current_app.send_static_file("index.html")


@root.route("/css/<path:path>")
def static_css(path):
    return send_from_directory(static_folder + "/css", path)


@root.route("/js/<path:path>")
def __tmp3(path):
    return send_from_directory(static_folder + "/js", path)


def _config_cors(cors_origins: List[str], testing):
    if cors_origins:
        logger.warning(
            "Running with additional allowed CORS origins specified through config "
            "or CLI argument (could be a security risk): {}".format(cors_origins)
        )

    if testing:
        # Used for development of aw-webui
        cors_origins.append("http://127.0.0.1:27180/*")

    # TODO: This could probably be more specific
    #       See https://github.com/ActivityWatch/aw-server/pull/43#issuecomment-386888769
    cors_origins.append("moz-extension://*")

    # See: https://flask-cors.readthedocs.org/en/latest/
    CORS(current_app, resources={r"/api/*": {"origins": cors_origins}})


# Only to be called from aw_server.main function!
def __tmp4(
    __tmp1,
    host: <FILL>,
    port,
    testing: __typ1 = False,
    cors_origins: List[str] = [],
    custom_static: Dict[str, str] = dict(),
):
    app = __typ2(
        host,
        testing=testing,
        __tmp1=__tmp1,
        cors_origins=cors_origins,
        custom_static=custom_static,
    )
    try:
        app.run(
            debug=testing,
            host=host,
            port=port,
            request_handler=FlaskLogHandler,
            use_reloader=False,
            threaded=True,
        )
    except OSError as e:
        logger.exception(e)
        raise e
