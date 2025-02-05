from operator import truediv

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from util.models import TimestampModel


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_active = True
        user.is_admin = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField('nickname', unique=True, max_length=20)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers',
                                       through='UserFollowing', through_fields=('from_user','to_user'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property  # abstractBaseUser 기본유저
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

class UserFollowing(TimestampModel):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followers')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')

    class Meta:
        unique_together = ('to_user', 'from_user')
