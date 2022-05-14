import typing

from ._chain_proxy import DataProxy


def dataclass_proxy(data_object: typing.Any) -> DataProxy:
    return DataProxy(data_object)


def get_value(proxy_object: DataProxy) -> typing.Any:
    return proxy_object()
