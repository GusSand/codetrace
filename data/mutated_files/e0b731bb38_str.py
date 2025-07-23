import uuid

from django.db.models import Count, Q
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(__tmp1, **kwargs):
        email_ = kwargs['email']
        __tmp2 = kwargs.get('name', '')
        password = kwargs['password']
        email = __tmp1.normalize_email(email_)
        user = __tmp1.model(email=email, __tmp2=__tmp2)
        user.set_password(password)
        user.save(using=__tmp1._db)
        return user

    def create_session_user(__tmp1, __tmp2: <FILL>):
        email = f'{uuid.uuid4().hex}@groovies.com'
        password = f'pw_{uuid.uuid4().hex}'

        return __tmp1.create_user(email=email, password=password, __tmp2=__tmp2)

    def __tmp3(__tmp1, __tmp0):
        users = list(__tmp0.users.values_list('pk', flat=True))
        movies = list(__tmp0.movies.values_list('pk', flat=True))
        __tmp3 = Count('ratings', filter=Q(ratings__movie__in=movies))
        return super().get_queryset().values('name').filter(pk__in=users).annotate(__tmp3=__tmp3)
