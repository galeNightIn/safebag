# safebag
[![Stable Version](https://img.shields.io/pypi/v/safebag?color=black)](https://pypi.org/project/safebag/)
[![tests](https://github.com/galeNightIn/safebag/workflows/tests/badge.svg)](https://github.com/galeNightIn/safebag)

_Safebag_ is a little python package implementing optional chaining.

## Installation

```bash
pip install safebag
```

## Usage

Code we want to avoid

```python
if (
    obj is not None 
    and obj.attr is not None 
    and obj.attr.attr is not None 
    and obj.attr.attr.attr is not None 
    and obj.attr.attr.attr.attr is not None
):
    # Do something useful with obj.attr.attr.attr.attr
    ...
```

Pythonic solution

```python
try:
    print(obj.attr.attr.attr.attr)
    # Do something useful with obj.attr.attr.attr.attr
except(NameError, AttributeError) as e:
    # Do something useful with an error
```

Still it's not very clean way in case of multiple attribute handling in one place
```python
try:
    print(obj.attr.attr.attr.attr)
    # Do something useful with obj.attr.attr.attr.attr
except(NameError, AttributeError) as e:
    ...

try:
    print(obj.attr.attr)
    # Do something useful with obj.attr.attr
except(NameError, AttributeError) as e:
    ...
    
try:
    print(obj.attr)
    # Do something useful with obj.attr
except(NameError, AttributeError) as e:
    ...
```

Usage example:
```python
from safebag import chain, get_value

if attr := chain(obj).attr.attr.attr.attr:
    # Do something useful with obj.attr.attr.attr.attr
    print(get_value(attr))

if attr := chain(obj).attr.attr:
    # Do something useful with obj.attr.attr
    print(get_value(attr))

if attr := chain(obj).attr:
    # Do something useful with obj.attr
    print(get_value(attr))
```


## Examples

### chain [[source](https://github.com/galeNightIn/safebag/blob/69e241022b85b3f4566556f3e3e956d5a750eb20/safebag/_methods.py#L9)]

Optional chain constructor, may be constructed from any object

Chain is used for building sequence of null-safe attribute calls

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
