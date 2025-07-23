# -*- coding: utf-8 -*-

import mock

from typing import Any

from zerver.lib.attachments import user_attachments
from zerver.lib.test_classes import ZulipTestCase
from zerver.models import Attachment


class __typ0(ZulipTestCase):
    def setUp(__tmp0) -> None:
        user_profile = __tmp0.example_user('cordelia')
        __tmp0.attachment = Attachment.objects.create(
            file_name='test.txt', path_id='foo/bar/test.txt', owner=user_profile)

    def test_list_by_user(__tmp0) :
        user_profile = __tmp0.example_user('cordelia')
        __tmp0.login(user_profile.email)
        result = __tmp0.client_get('/json/attachments')
        __tmp0.assert_json_success(result)
        attachments = user_attachments(user_profile)
        __tmp0.assertEqual(result.json()['attachments'], attachments)

    def __tmp1(__tmp0) -> None:
        user_profile = __tmp0.example_user('cordelia')
        __tmp0.login(user_profile.email)
        with mock.patch('zerver.lib.attachments.delete_message_image', side_effect=Exception()):
            result = __tmp0.client_delete('/json/attachments/{id}'.format(id=__tmp0.attachment.id))
        __tmp0.assert_json_error(result, "An error occurred while deleting the attachment. Please try again later.")

    @mock.patch('zerver.lib.attachments.delete_message_image')
    def __tmp2(__tmp0, __tmp4: <FILL>) -> None:
        user_profile = __tmp0.example_user('cordelia')
        __tmp0.login(user_profile.email)
        result = __tmp0.client_delete('/json/attachments/{id}'.format(id=__tmp0.attachment.id))
        __tmp0.assert_json_success(result)
        attachments = user_attachments(user_profile)
        __tmp0.assertEqual(attachments, [])

    def test_list_another_user(__tmp0) :
        user_profile = __tmp0.example_user('iago')
        __tmp0.login(user_profile.email)
        result = __tmp0.client_get('/json/attachments')
        __tmp0.assert_json_success(result)
        __tmp0.assertEqual(result.json()['attachments'], [])

    def __tmp3(__tmp0) -> None:
        user_profile = __tmp0.example_user('iago')
        __tmp0.login(user_profile.email)
        result = __tmp0.client_delete('/json/attachments/{id}'.format(id=__tmp0.attachment.id))
        __tmp0.assert_json_error(result, 'Invalid attachment')
        user_profile_to_remove = __tmp0.example_user('cordelia')
        attachments = user_attachments(user_profile_to_remove)
        __tmp0.assertEqual(attachments, [__tmp0.attachment.to_dict()])

    def __tmp5(__tmp0) :
        result = __tmp0.client_get('/json/attachments')
        __tmp0.assert_json_error(result, 'Not logged in: API authentication or user session required', status_code=401)

    def test_delete_unauthenticated(__tmp0) -> None:
        result = __tmp0.client_delete('/json/attachments/{id}'.format(id=__tmp0.attachment.id))
        __tmp0.assert_json_error(result, 'Not logged in: API authentication or user session required', status_code=401)
