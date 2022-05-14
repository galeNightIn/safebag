import typing

from ._chain_proxy import ChainProxy


def dataclass_proxy(data_object: typing.Any) -> ChainProxy:
    return ChainProxy(data_object)


def get_value(proxy_object: ChainProxy) -> typing.Any:
    return proxy_object()
