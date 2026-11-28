"""Regression test for https://github.com/typeddjango/django-stubs/issues/2911.

A TypeVar with a forward-referenced bound used in a QuerySet subclass
caused 'Must not defer during final iteration' crash in mypy.
"""

from __future__ import annotations

from typing import assert_type

from django.db import models
from django.db.models.query import QuerySet
from typing_extensions import TypeVar

T = TypeVar("T", bound="MyModel")


class MyModelQuerySet(QuerySet[T]):
    pass


class MyModel(models.Model):
    class Meta:
        app_label = "myapp"


class CustomManager(models.Manager["OtherModel"]):
    def manager_method(self) -> str:
        return ""


class OtherQuerySet(models.QuerySet["OtherModel"]): ...


class OtherModel(models.Model):
    class Meta:
        app_label = "myapp"


# `from_queryset` returns a `Manager` of the queryset class. Only the mypy plugin keeps the manager subclass and
# its members: typing can't spell "`cls` re-parametrized with another queryset type"
# The mypy plugin only builds the generated class for an assignment, `NewManager = CustomManager.from_queryset(...)`
assert_type(CustomManager.from_queryset(OtherQuerySet)().all(), OtherQuerySet)  # type: ignore[assert-type]
assert_type(CustomManager.from_queryset(OtherQuerySet)().get(), OtherModel)
CustomManager.from_queryset(OtherQuerySet)().manager_method()  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # ty: ignore[missing-attribute]  # pyrefly: ignore[missing-attribute]


def managers_are_not_querysets(manager: models.Manager[OtherModel]) -> None:
    len(manager)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
    manager[0]  # type: ignore[index]  # pyright: ignore[reportIndexIssue]  # pyrefly: ignore[bad-index]  # ty: ignore[not-subscriptable]
    manager.delete()  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[missing-attribute]
