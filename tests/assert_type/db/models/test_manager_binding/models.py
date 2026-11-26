"""A manager declared without type arguments is bound to the model it is accessed through."""

from __future__ import annotations

from typing import assert_type

from django.db import models
from django.db.models.query import QuerySet


class BookManager(models.Manager):  # pyright: ignore[reportMissingTypeArgument]
    def by_author(self) -> int:
        return 0


class BookQuerySet(models.QuerySet["Book"]):
    def published(self) -> BookQuerySet:
        return self


class Book(models.Model):
    objects = models.Manager()  # pyright: ignore[reportUnknownVariableType]
    custom = BookManager()
    explicit: models.Manager[Book] = models.Manager()
    generated = models.Manager.from_queryset(BookQuerySet)()  # pyright: ignore[reportUnknownVariableType]


class Novel(Book):
    pass


class Publication(models.Model):
    objects = models.Manager()  # pyright: ignore[reportUnknownVariableType]

    class Meta:
        abstract = True


class Magazine(Publication):
    pass


def plain_manager_is_bound_to_its_model() -> None:
    assert_type(Book.objects, models.Manager[Book])
    assert_type(Book.objects.get(), Book)
    assert_type(Book.objects.filter(), QuerySet[Book])


def plain_manager_is_bound_to_the_subclass() -> None:
    assert_type(Novel.objects.get(), Novel)
    assert_type(Magazine.objects.get(), Magazine)


def custom_manager_without_type_arguments_is_bound_to_its_model() -> None:
    assert_type(Book.custom.get(), Book)
    # Binding returns a plain `Manager`: typing can't re-parametrize `Self` with the model
    assert_type(Book.custom.by_author(), int)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportAssertTypeFailure]  # ty: ignore[missing-attribute, type-assertion-failure]  # pyrefly: ignore[missing-attribute, assert-type]


def from_queryset_manager_without_model_is_bound_to_its_model() -> None:
    assert_type(Book.generated.get(), Book)
    # ... and drops the queryset type param, for the same reason
    assert_type(Book.generated.all(), BookQuerySet)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]


def explicit_manager_type_is_kept() -> None:
    assert_type(Book.explicit.get(), Book)
    # Django binds the inherited manager to `Novel`, the declared type says `Book`
    assert_type(Novel.explicit.get(), Book)
