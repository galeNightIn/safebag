# safebag
[![Stable Version](https://img.shields.io/pypi/v/safebag?color=black)](https://pypi.org/project/safebag/)
[![tests](https://github.com/galeNightIn/safebag/workflows/tests/badge.svg)](https://github.com/galeNightIn/safebag)

_Safebag_ is a little python package implementing optional chaining.

## Installation

```bash
pip install safebag
```

## Usage

### chain [[source](https://github.com/galeNightIn/safebag/blob/69e241022b85b3f4566556f3e3e956d5a750eb20/safebag/_methods.py#L9)]

Optional chain constructor

Optional chain constructed from any object.

Chain is used for building sequence of null-safe attribute calls.

```python
from __future__ import annotations

import dataclasses as dt
import typing


@dt.dataclass
class Node:
    data: int
    node: typing.Optional[Node]


nodes = Node(data=1, node=Node(data=2, node=None))

from safebag import chain

third_node_proxy = chain(nodes).node.node.node
print(third_node_proxy)  # ChainProxy(data_object=None, bool_hook=False)
```

### get_value [[source](https://github.com/galeNightIn/safebag/blob/69e241022b85b3f4566556f3e3e956d5a750eb20/safebag/_methods.py#L39)]

Final value getter for optional chain.

Optional chain constructed from any object. Chain is used for building sequence of null-safe attribute calls.

```python
from __future__ import annotations

import dataclasses as dt
import typing


@dt.dataclass
class Node:
    data: int
    node: typing.Optional[Node]


nodes = Node(data=1, node=Node(data=2, node=None))

from safebag import chain, get_value

third_node_proxy = chain(nodes).node.node.node
value = get_value(third_node_proxy)
assert value is None

next_node = chain(nodes).node
value = get_value(next_node)  # Node(data=2, node=None)
```

Possible way of getting value
```python
if next_node := chain(nodes).node:
    print(next_node.get_value())  # Node(data=2, node=None)
```

Default can be passed as argument
```python
if next_node := chain(nodes).node.node:
    print(next_node.get_value(default='Default')) # 'Default'
```


Useful in combination with walrus operator:

```python
if next_node := chain(nodes).node.node:
    print(get_value(next_node))

if next_node := chain(nodes).node:
    print(get_value(next_node))  # Node(data=2, node=None)
```

### ChainProxy [[source](https://github.com/galeNightIn/safebag/blob/69e241022b85b3f4566556f3e3e956d5a750eb20/safebag/_chain_proxy.py#L11)]

`ChainProxy` container:
* stores `data_object`
* proxying `data_object` attribute value into new `ChainProxy` instance
when attribute is invoked. If attribute does not exist or attribute value is `None`.
`ChainProxy` instance `data_object` will be `None` and `bool_hook` will be `False`.
* `ChainProxy` instance always returning when attribute is invoked.