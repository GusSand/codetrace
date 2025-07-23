from typing import TypeAlias
__typ0 : TypeAlias = "int"
#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

from datetime import timedelta

from flask import Flask

from easyjwt import EasyJWTError
from flask_easyjwt import FlaskEasyJWT


class AccountValidationToken(FlaskEasyJWT):

    def __init__(__tmp2, key=None):
        super().__init__(key)

        __tmp2.user_id = None


class IntegrationTest(TestCase):

    # region Flask App

    def _create_app(__tmp2) -> Flask:
        """
            Create a Flask test application.

            :return: The newly created application instance.
        """

        application = Flask(__name__)
        application.config.from_mapping(
            EASYJWT_KEY=__tmp2.easyjwt_key,
            EASYJWT_TOKEN_VALIDITY=__tmp2.validity,
            SECRET_KEY=__tmp2.secret_key,
        )

        application.add_url_rule('/get_token/<int:user_id>', view_func=__tmp2._get_token)
        application.add_url_rule('/validate_user/<string:token>', view_func=__tmp2._validate_user)

        return application

    @staticmethod
    def _get_token(user_id) :
        """
            Get an account validation token.

            :param user_id: The value of the `user_id` claim.
            :return: The created token.
        """

        __tmp3 = AccountValidationToken()
        __tmp3.user_id = user_id

        return __tmp3.create()

    @staticmethod
    def _validate_user(__tmp3: <FILL>):
        """
            Verify the user given in the given account validation token.

            :param token: A JWT created with :class:`AccountValidationToken`.
            :return: The user ID of the validated user on success, 0 on failure - both as a string.
        """

        try:
            __tmp3 = AccountValidationToken.verify(__tmp3)
            user_id = __tmp3.user_id
        except EasyJWTError:
            user_id = 0

        return str(user_id)

    # endregion

    # region Test Setup

    def setUp(__tmp2):
        """
            Prepare the test cases.
        """

        __tmp2.easyjwt_key = 'abcdefghijklmnopqrstuvwxyz'
        __tmp2.secret_key = __tmp2.easyjwt_key[::-1]
        __tmp2.validity = timedelta(minutes=5)

        __tmp2.app = __tmp2._create_app()
        __tmp2.client = __tmp2.app.test_client()
        __tmp2.app_context = __tmp2.app.app_context()
        __tmp2.app_context.push()
        __tmp2.request_context = __tmp2.app.test_request_context()
        __tmp2.request_context.push()

    def __tmp0(__tmp2):
        """
            Clean up after each test case.
        """

        __tmp2.request_context.pop()
        __tmp2.app_context.pop()

    # endregion

    def __tmp1(__tmp2):
        """
            Test validating a token that is not valid.

            Expected Result: The token is rejected.
        """

        # Use a different key for creating the token then for validating it.
        token_object = AccountValidationToken(__tmp2.easyjwt_key[::-1])
        token_object.user_id = 42
        __tmp3 = token_object.create()

        response = __tmp2.client.get(f'/validate_user/{__tmp3}')
        validated_user = response.get_data(as_text=True)
        __tmp2.assertEqual(str(0), validated_user)

    def test_validate_success(__tmp2):
        """
            Test getting and successfully validating a token.

            Expected Result: A token can be requested from the app and then successfully validated.
        """

        user_id = 42
        response = __tmp2.client.get(f'/get_token/{user_id}')
        __tmp3 = response.get_data(as_text=True)
        __tmp2.assertIsNotNone(__tmp3)

        response = __tmp2.client.get(f'/validate_user/{__tmp3}')
        validated_user = response.get_data(as_text=True)
        __tmp2.assertEqual(str(user_id), validated_user)
