from __future__ import annotations

from typing import Any, assert_type

from django.conf import settings


def default_settings_are_typed() -> None:
    assert_type(settings.DEBUG, bool)
    assert_type(settings.AUTH_USER_MODEL, str)
    assert_type(settings.DATABASES, dict[str, dict[str, Any]])


def project_settings_override_the_default_type() -> None:
    # Only the mypy plugin reads the project's settings module, which sets `STATIC_URL = "static/"`.
    # TODO: https://github.com/typeddjango/django-stubs/issues/579
    assert_type(settings.STATIC_URL, str)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]


def unknown_settings_fall_back_to_any() -> None:
    settings.MY_SETTING  # type: ignore[misc]
