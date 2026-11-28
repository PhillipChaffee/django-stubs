from typing import Any, ClassVar, Self

from django.contrib.flatpages.models import FlatPage
from django.contrib.redirects.models import Redirect
from django.db import models
from django.db.models.fields.related_descriptors import ManyToManyDescriptor, ReverseManyToOneDescriptor
from django.http.request import HttpRequest
from typing_extensions import TypeVar

SITE_CACHE: Any

_SiteT = TypeVar("_SiteT", bound=Site)

class SiteManager(models.Manager[_SiteT]):
    # `SITE_CACHE` is shared by every `Site` subclass, so a cached parent instance can be returned.
    def get_current(self, request: HttpRequest | None = ...) -> Site: ...
    def clear_cache(self) -> None: ...
    def get_by_natural_key(self, domain: str) -> _SiteT: ...

class Site(models.Model):
    objects: ClassVar[SiteManager[Self]]

    domain: models.CharField[str | int, str]
    name: models.CharField[str | int, str]
    # Reverse accessors of `Redirect.site` and `FlatPage.sites`, only added when
    # `django.contrib.redirects` and `django.contrib.flatpages`, respectively, are installed.
    redirect_set: ClassVar[ReverseManyToOneDescriptor[Redirect]]
    flatpage_set: ClassVar[ManyToManyDescriptor[FlatPage]]
    def natural_key(self) -> tuple[str]: ...

def clear_site_cache(sender: type[Site], **kwargs: Any) -> None: ...
