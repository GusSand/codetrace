from typing import TypeAlias
__typ0 : TypeAlias = "Response"
# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import Flask, url_for, redirect, session, flash
import flask_login
from werkzeug.wrappers import Response

from database import init_db
# from views.user import user_mod, set_hash
# from models import User
import views

APP = Flask(__name__)
APP.config.from_pyfile('musicresults.cfg')
init_db(APP)
# set_hash(APP.config.get('PWD_SALT'))

APP.register_blueprint(views.band, url_prefix='/band')
APP.register_blueprint(views.contest, url_prefix='/contest')
APP.register_blueprint(views.contribute, url_prefix='/contribute')
APP.register_blueprint(views.index)
APP.register_blueprint(views.person, url_prefix='/person')
APP.register_blueprint(views.testpiece, url_prefix='/test-piece')
APP.register_blueprint(views.user, url_prefix='/user')
APP.register_blueprint(views.venue, url_prefix='/venue')

LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.init_app(APP)


@APP.teardown_appcontext
def __tmp1(_: Exception = None) -> None:
    # shutdown sqlalchemy session
    from database import get_db_session
    get_db_session().remove()


# @LOGIN_MANAGER.user_loader
# def user_loader(username: str):
#     uid = '_'.join(username.split('_')[1:])
#     user = None
#
#     if username.startswith('user'):
#         user = User.filter_by(username=uid).first()
#     elif username.startswith('tester'):
#         user = Tester.filter_by(id=uid).first()
#
#     return user


@APP.before_request
def make_session_permanent() -> None:
    session.permanent = True
    if flask_login.current_user.is_authenticated and flask_login.current_user.is_admin():
        APP.permanent_session_lifetime = timedelta(minutes=60)
    else:
        APP.permanent_session_lifetime = timedelta(minutes=15)


@APP.errorhandler(401)
def not_authorized(__tmp0: <FILL>) :
    flash('請重新登入', 'info')
    print(__tmp0)
    return redirect(url_for('test_mod.login'))


if __name__ == '__main__':
    if APP.config.get('RUNNING_MODE') == 'debug':
        APP.run(
            host=APP.config.get('HOST', 'localhost'),
            port=APP.config.get('PORT', 8080)
        )
    else:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        HTTP_SERVER = HTTPServer(WSGIContainer(APP))
        HTTP_SERVER.listen(APP.config.get('PORT', 8080))
        IOLoop.instance().start()
