# mypy treats any name `MYPY` as true. Declared as `bool`, not `Literal[False]`, so that ty also sees the
# typed branch, e.g. the nested `Meta` classes, and accepts a subclass's own `class Meta:` as an override.
MYPY: bool
