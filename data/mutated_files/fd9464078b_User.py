from rest_framework import serializers

from .models import User


class __typ0(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj: <FILL>):
        return obj.create_jwt()

    def create(self, __tmp0):
        return User.objects.create_session_user(__tmp0['name'])

    class Meta:
        model = User
        fields = ('name', 'token')
