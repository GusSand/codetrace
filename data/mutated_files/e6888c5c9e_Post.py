from marshmallow import fields, Schema

from meerkat.domain.post.entities import Post


class __typ1(Schema):
    class __typ0:
        ordered = True

    id: fields.Str = fields.Str()
    title: fields.Str = fields.Str(required=True)
    body: fields.Str = fields.Str(required=True)

    @classmethod
    def __tmp0(__tmp1, post: <FILL>):
        object = __tmp1()
        return object.load({
            "id": str(post.id),
            "title": str(post.title),
            "body": str(post.body)
        })


class AddNewPostSchema(Schema):
    class __typ0:
        ordered = True

    title: fields.Str = fields.Str(required=True)
    body: fields.Str = fields.Str(required=True)
