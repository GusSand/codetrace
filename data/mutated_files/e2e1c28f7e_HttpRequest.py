from django.http.request import HttpRequest
from rest_framework.filters import BaseFilterBackend
from rest_framework.compat import coreapi, coreschema
from rest_framework.serializers import ValidationError


class __typ0(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def __tmp2(__tmp1, request, __tmp3, __tmp0):
        if not request.query_params.get('my'):
            return __tmp3

        if request.user.is_anonymous:
            raise ValidationError('必须登录才能查看我的帖子')

        return __tmp3.filter(createdBy_id=request.user.id)

    def __tmp4(__tmp1, __tmp0):
        return [
            coreapi.Field(
                name='my',
                required=False,
                location='query',
                schema=coreschema.Boolean(
                    title='只看我的',
                    description='如果设置为 true，只返回我的帖子。默认为 false',
                )
            )
        ]


class __typ1(BaseFilterBackend):
    """
    Filter the posts belonged to assigned tags.
    """

    def __tmp2(__tmp1, request: HttpRequest, __tmp3, __tmp0):
        if not request.query_params.get('tagid'):
            return __tmp3

        return __tmp3.filter(tag=request.query_params.get('tagid'))

    def __tmp4(__tmp1, __tmp0):
        return [
            coreapi.Field(
                name='tagid',
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Post标签id',
                    description='选择标签后，只返回对应标签的posts',
                )
            )
        ]


class NoImgFilter(BaseFilterBackend):
    def __tmp2(__tmp1, request: <FILL>, __tmp3, __tmp0):
        # we do noting here. because it will be read by ReadContentSerializer
        return __tmp3

    def __tmp4(__tmp1, __tmp0):
        return [
            coreapi.Field(
                name='noimg',
                required=False,
                location='query',
                schema=coreschema.Boolean(
                    title='不返回图片',
                    description='在返回的列表里不返回图片，这样设置可以提高查询速度。（默认为false）',
                )
            )
        ]
