from typing import TypeAlias
__typ2 : TypeAlias = "Flask"
__typ1 : TypeAlias = "str"
#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

from datetime import timedelta

from flask import Flask

from easyjwt import EasyJWTError
from flask_easyjwt import FlaskEasyJWT


class __typ0(FlaskEasyJWT):

    def __init__(__tmp1, key=None):
        super().__init__(key)

        __tmp1.user_id = None


class __typ3(TestCase):

    # region Flask App

    def _create_app(__tmp1) :
        """
            Create a Flask test application.

            :return: The newly created application instance.
        """

        application = __typ2(__name__)
        application.config.from_mapping(
            EASYJWT_KEY=__tmp1.easyjwt_key,
            EASYJWT_TOKEN_VALIDITY=__tmp1.validity,
            SECRET_KEY=__tmp1.secret_key,
        )

        application.add_url_rule('/get_token/<int:user_id>', view_func=__tmp1._get_token)
        application.add_url_rule('/validate_user/<string:token>', view_func=__tmp1._validate_user)

        return application

    @staticmethod
    def _get_token(user_id: <FILL>) -> __typ1:
        """
            Get an account validation token.

            :param user_id: The value of the `user_id` claim.
            :return: The created token.
        """

        __tmp2 = __typ0()
        __tmp2.user_id = user_id

        return __tmp2.create()

    @staticmethod
    def _validate_user(__tmp2):
        """
            Verify the user given in the given account validation token.

            :param token: A JWT created with :class:`AccountValidationToken`.
            :return: The user ID of the validated user on success, 0 on failure - both as a string.
        """

        try:
            __tmp2 = __typ0.verify(__tmp2)
            user_id = __tmp2.user_id
        except EasyJWTError:
            user_id = 0

        return __typ1(user_id)

    # endregion

    # region Test Setup

    def __tmp4(__tmp1):
        """
            Prepare the test cases.
        """

        __tmp1.easyjwt_key = 'abcdefghijklmnopqrstuvwxyz'
        __tmp1.secret_key = __tmp1.easyjwt_key[::-1]
        __tmp1.validity = timedelta(minutes=5)

        __tmp1.app = __tmp1._create_app()
        __tmp1.client = __tmp1.app.test_client()
        __tmp1.app_context = __tmp1.app.app_context()
        __tmp1.app_context.push()
        __tmp1.request_context = __tmp1.app.test_request_context()
        __tmp1.request_context.push()

    def __tmp0(__tmp1):
        """
            Clean up after each test case.
        """

        __tmp1.request_context.pop()
        __tmp1.app_context.pop()

    # endregion

    def __tmp5(__tmp1):
        """
            Test validating a token that is not valid.

            Expected Result: The token is rejected.
        """

        # Use a different key for creating the token then for validating it.
        token_object = __typ0(__tmp1.easyjwt_key[::-1])
        token_object.user_id = 42
        __tmp2 = token_object.create()

        response = __tmp1.client.get(f'/validate_user/{__tmp2}')
        validated_user = response.get_data(as_text=True)
        __tmp1.assertEqual(__typ1(0), validated_user)

    def __tmp3(__tmp1):
        """
            Test getting and successfully validating a token.

            Expected Result: A token can be requested from the app and then successfully validated.
        """

        user_id = 42
        response = __tmp1.client.get(f'/get_token/{user_id}')
        __tmp2 = response.get_data(as_text=True)
        __tmp1.assertIsNotNone(__tmp2)

        response = __tmp1.client.get(f'/validate_user/{__tmp2}')
        validated_user = response.get_data(as_text=True)
        __tmp1.assertEqual(__typ1(user_id), validated_user)
