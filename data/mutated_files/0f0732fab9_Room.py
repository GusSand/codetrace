from typing import Dict, List, Optional

from rest_framework import serializers

from users.models import User
from movies.serializers import MovieSerializer
from .exceptions import RoomUsersNotReady
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField(read_only=True)
    movies = MovieSerializer(many=True, read_only=True)
    unrated_movies = serializers.SerializerMethodField(read_only=True)

    @property
    def user(__tmp0) :
        try:
            return __tmp0.context['request'].user
        except KeyError:
            return None

    def get_users(__tmp0, room: Room) -> List[Dict]:
        return list(room.users.rated_count(room))

    def get_unrated_movies(__tmp0, room: <FILL>) :
        qs = room.movies.unrated(user=__tmp0.user)
        return MovieSerializer(qs, many=True).data

    def update(__tmp0, instance, validated_data):
        instance.sync_user(__tmp0.context['request'].user)
        return super().update(instance, validated_data)

    def create(__tmp0, validated_data):
        return __tmp0.Meta.model.objects.create_room(admin=__tmp0.context['request'].user, **validated_data)

    class Meta:
        model = Room
        fields = ('slug', 'mood', 'admin', 'users', 'movies', 'unrated_movies')
        read_only_fields = ('admin', )


class RoomResultsSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField(read_only=True)

    def get_results(__tmp0, room):
        try:
            qs = room.get_or_create_results()
        except RoomUsersNotReady:
            raise serializers.ValidationError('room users are not ready for results')

        return MovieSerializer(qs, many=True).data

    class Meta:
        model = Room
        fields = ('slug', 'results')
        read_only_fields = ('slug',)
