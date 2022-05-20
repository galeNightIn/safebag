from __future__ import annotations

import typing

T = typing.TypeVar("T")
V = typing.TypeVar("V")

_DATA_PROXY_SLOTS = ("__data_obj__", "__bool_hook__")


class ChainProxy(typing.Generic[T]):
    """
    `ChainProxy` container:
        * stores `data_object`
        * proxying `data_object` attribute value into new `ChainProxy` instance
        when attribute is invoked. If attribute does not exist or attribute value is `None`
        `ChainProxy` instance `data_object` will be `None` and `bool_hook` will be `False`.

    `ChainProxy` instance always returning when attribute is invoked

    :param data_object: Data proxied by `ChainProxy`
    :type data_object: T
    :param: bool_hook: Used in `ChainProxy` instance bool cast.
    bool(chain_proxy_instance) == bool_hook
    :type: bool
    """

    __slots__ = _DATA_PROXY_SLOTS

    def __init__(self, data_object: T, *, bool_hook: bool = False) -> None:
        self.__data_obj__ = data_object
        self.__bool_hook__ = bool_hook

    def __getattr__(self, attr: str) -> ChainProxy[T]:
        object_attribute = getattr(self.__data_obj__, attr, None)

        if object_attribute is None:
            return ChainProxy(
                typing.cast(T, object_attribute),
                bool_hook=False,
            )

        return ChainProxy(object_attribute, bool_hook=True)

    def get_value(self, *, default: typing.Optional[V] = None) -> typing.Union[T, V]:
        if not self and default is not None:
            return default
        return self.__data_obj__

    def __bool__(self) -> bool:
        return self.__bool_hook__

    def __repr__(self) -> str:
        return f"DataProxy(data_object={self.__data_obj__}, bool_hook={self.__bool_hook__})"

    def __str__(self) -> str:
        return f"data_object={self.__data_obj__}, bool_hook={self.__bool_hook__}"


def _get_value(
    chain_proxy: ChainProxy[T], *, default: typing.Optional[V] = None
) -> typing.Union[T, V]:
    """Protected method for withdrawal object from `ChainProxy`
    :param chain_proxy: `ChainProxy` instance
    :type chain_proxy: ChainProxy[T]
    :param default: Value returned if object is None (default is None)
    :type default: Optional[V]
    :returns: data_object from `ChainProxy`
    :rtype: T or V
    """
    return chain_proxy.get_value(default=default)
