from __future__ import annotations

import typing

_DATA_PROXY_SLOTS = ("__data_obj__", "__bool_hook__")

T = typing.TypeVar("T")


class DataProxy(typing.Generic[T]):
    __slots__ = _DATA_PROXY_SLOTS

    def __init__(self, data_object: T, *, bool_hook: bool = False) -> None:
        self.__data_obj__ = data_object
        self.__bool_hook__ = bool_hook

    def __getattr__(self, attr: str) -> DataProxy[T]:
        object_attribute = getattr(self.__data_obj__, attr, None)

        if object_attribute is None:
            return DataProxy(object_attribute, bool_hook=False)

        return DataProxy(object_attribute, bool_hook=True)

    def __bool__(self) -> bool:
        return self.__bool_hook__

    def __call__(self) -> T:
        return self.__data_obj__

    def __repr__(self) -> str:
        return f"DataProxy(data_object={self.__data_obj__}, bool_hook={self.__bool_hook__})"

    def __str__(self) -> str:
        return f"data_object={self.__data_obj__}, bool_hook={self.__bool_hook__}"
