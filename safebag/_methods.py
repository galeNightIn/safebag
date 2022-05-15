import typing

from ._chain_proxy import ChainProxy, _get_value

T = typing.TypeVar("T")
V = typing.TypeVar("V")


def chain(data_object: T) -> ChainProxy[T]:
    """Optional chain constructor

    Optional chain constructed from any object.
    Chain is used for building sequence of null-safe attribute calls.

    :Example:
        >>> from __future__ import annotations
        >>> import dataclasses as dt
        >>> import typing
        >>> @dt.dataclass
        ... class Node:
        ...     data: int
        ...     node: typing.Optional[Node]
        >>> nodes = Node(data=1, node=Node(data=2, node=None))
        >>>
        >>> from safebag import chain
        >>> from safebag import chain, get_value
        >>> third_node_proxy = chain(nodes).node.node.node
        >>> third_node_proxy
        ChainProxy(data_object=None, bool_hook=False)

    :param data_object: Any object for optional chaining
    :type data_object: T
    :return: `ChainProxy` for data_object
    :rtype ChainProxy[T]
    """
    return ChainProxy(data_object)


def get_value(
    proxy_object: ChainProxy, *, default: typing.Optional[V] = None
) -> typing.Union[T, V, None]:
    """Final value getter for optional chain.

    Optional chain constructed from any object.
    Chain is used for building sequence of null-safe attribute calls.

    :Example:
        >>> from __future__ import annotations
        >>> import dataclasses as dt
        >>> import typing
        >>> @dt.dataclass
        ... class Node:
        ...     data: int
        ...     node: typing.Optional[Node]
        >>> nodes = Node(data=1, node=Node(data=2, node=None))
        >>>
        >>> from safebag import chain
        >>> from safebag import chain, get_value
        >>> third_node_proxy = chain(nodes).node.node.node

        >>> value = get_value(third_node_proxy)
        >>> assert value is None

        >>> next_node = chain(nodes).node
        >>> value = get_value(next_node)
        >>> value
        Node(data=2, node=None)

    :Useful in combination with walrus operator:
        >>> if next_node := chain(nodes).node.node:
        ...     print(get_value(next_node))
        >>> if next_node := chain(nodes).node:
        ...     print(get_value(next_node))
        Node(data=2, node=None)
    """
    return _get_value(proxy_object, default=default)
