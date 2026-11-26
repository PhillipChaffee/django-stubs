from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class Member(AbstractUser):
    class Meta:
        verbose_name = "member"


class InheritedMetaMember(AbstractUser):
    class Meta(AbstractUser.Meta):
        ordering = ("username",)


class MinimalUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "minimal user"


class InheritedMetaMinimalUser(AbstractBaseUser, PermissionsMixin):
    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):
        verbose_name = "minimal user"


class MemberCreationForm(UserCreationForm[Member]):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")


class MemberChangeForm(UserChangeForm[Member]):
    # Unlike models, no stub declaration of `UserChangeForm.Meta` satisfies both pyrefly
    # (wants a `ClassVar`) and ty (rejects one) for a form's own `class Meta:`.
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]  # ty: ignore[incompatible-attribute-override]  # pyrefly: ignore[bad-override]
        model = Member
        fields = "__all__"
