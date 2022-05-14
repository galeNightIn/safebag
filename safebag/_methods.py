import typing

from ._chain_proxy import ChainProxy, _get_value

T = typing.TypeVar('T')
V = typing.TypeVar('V')


def chain(data_object: T) -> ChainProxy[T]:
    return ChainProxy(data_object)


def get_value(
        proxy_object: ChainProxy,
        *,
        default: typing.Optional[V] = None
) -> typing.Union[T, V, None]:
    return _get_value(proxy_object, default=default)
