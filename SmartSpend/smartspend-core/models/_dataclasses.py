"""Compatibility helpers for compact SmartSpend data models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


def slotted_dataclass(
    cls: type | None = None, *, frozen: bool = False
) -> type | Callable[[type], type]:
    """Provide ``dataclass(slots=True)`` behavior on Python 3.9 and later."""

    def decorate(target: type) -> type:
        decorated = dataclass(target, frozen=frozen)
        namespace = dict(decorated.__dict__)

        # Slot descriptors cannot coexist with class-level defaults used while
        # dataclass builds ``__init__``. The initializer retains those defaults.
        for name in decorated.__dataclass_fields__:
            namespace.pop(name, None)

        namespace.pop("__dict__", None)
        namespace.pop("__weakref__", None)
        namespace["__slots__"] = tuple(decorated.__dataclass_fields__)
        if frozen:
            field_names = tuple(decorated.__dataclass_fields__)

            def __reduce__(self):
                return (type(self), tuple(getattr(self, name) for name in field_names))

            namespace["__reduce__"] = __reduce__
        return type(decorated)(decorated.__name__, decorated.__bases__, namespace)

    return decorate if cls is None else decorate(cls)
