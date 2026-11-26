from __future__ import annotations

import datetime
from collections.abc import AsyncIterator, Iterator
from typing import Any, assert_type

from django.db import models
from django.db.models.query import QuerySet, RawQuerySet
from django.utils import timezone


class Blog(models.Model):
    created_at = models.DateTimeField()


def queryset_methods_keep_the_row_type(qs: QuerySet[Blog], manager: models.Manager[Blog]) -> None:
    assert_type(qs.get(id=1), Blog)
    assert_type(iter(qs), Iterator[Blog])
    assert_type(qs.iterator(), Iterator[Blog])
    assert_type(qs.first(), Blog | None)
    assert_type(qs.earliest(), Blog)
    assert_type(qs[0], Blog)
    assert_type(qs[:9], QuerySet[Blog, Blog])
    assert_type(qs[1:9:None], QuerySet[Blog, Blog])
    # a step evaluates the queryset and returns a list
    assert_type(qs[::2], list[Blog])
    assert_type(qs[1:9:2], list[Blog])
    assert_type(qs.create(), Blog)
    assert_type(qs.get_or_create(), tuple[Blog, bool])
    assert_type(qs.exists(), bool)
    assert_type(qs.none(), QuerySet[Blog, Blog])
    assert_type(qs.update_or_create(), tuple[Blog, bool])
    assert_type(qs.explain(), str)
    assert_type(qs.raw(qs.explain()), RawQuerySet[Blog])
    assert_type(qs.raw(qs.explain())[0], Blog)
    assert_type(qs.raw(qs.explain())[:9], list[Blog])
    assert_type(qs.distinct(), QuerySet[Blog, Blog])
    assert_type(qs.distinct("created_at"), QuerySet[Blog, Blog])
    assert_type(qs & qs, QuerySet[Blog, Blog])
    # .dates / .datetimes swap the row type
    assert_type(manager.dates("created_at", "day"), QuerySet[Blog, datetime.date])
    assert_type(manager.datetimes("created_at", "day"), QuerySet[Blog, datetime.datetime])
    # defer / only
    assert_type(qs.defer("created_at"), QuerySet[Blog, Blog])
    assert_type(qs.defer(None), QuerySet[Blog, Blog])
    assert_type(qs.only("created_at"), QuerySet[Blog, Blog])
    qs.only(None)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
    # bulk methods
    assert_type(qs.count(), int)
    assert_type(qs.update(created_at=timezone.now()), int)
    assert_type(qs.in_bulk(), dict[Any, Blog])
    assert_type(qs.bulk_update(list(qs), fields=["created_at"]), int)
    assert_type(qs.bulk_create([]), list[Blog])
    assert_type(qs.delete(), tuple[int, dict[str, int]])


async def async_queryset_methods_keep_the_row_type(qs: QuerySet[Blog], manager: models.Manager[Blog]) -> None:
    assert_type(await qs.aget(id=1), Blog)
    assert_type(await qs.afirst(), Blog | None)
    assert_type(await qs.acreate(), Blog)
    assert_type(qs.aiterator(), AsyncIterator[Blog])
    assert_type(manager.aiterator(), AsyncIterator[Blog])
    async for blog in qs:
        assert_type(blog, Blog)


def values_list_row_shapes(field: str) -> None:
    # The mypy plugin resolves literal field names to the field types; these are the shapes without it
    assert_type(Blog.objects.values_list(field).get(), tuple[Any, ...])
    assert_type(Blog.objects.all().values_list(field, field).get(), tuple[Any, ...])
    assert_type(Blog.objects.values_list(field, flat=True).get(), Any)
    # `flat=True` without fields returns the primary keys, the mypy plugin resolves their type
    assert_type(Blog.objects.values_list(flat=True).get(), Any)  # type: ignore[assert-type]
    assert_type(Blog.objects.values_list(field, named=True).get(), Any)


def values_list_rejects_invalid_flag_combinations(field: str) -> None:
    # Django raises `TypeError` for both calls, they match the deprecated fallback overload
    Blog.objects.values_list(field, field, flat=True)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[deprecated]  # pyrefly: ignore[deprecated]
    # The mypy plugin reports its own error when it can read the arguments
    Blog.objects.all().values_list(field, flat=True, named=True)  # type: ignore[misc]  # pyright: ignore[reportDeprecated]  # ty: ignore[deprecated]  # pyrefly: ignore[deprecated]


def values_list_with_non_literal_flag_is_deprecated(field: str, flag: bool) -> None:
    assert_type(Blog.objects.values_list(field, flat=flag), QuerySet[Blog, Any])  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[deprecated]  # pyrefly: ignore[deprecated]
