from dataclasses import dataclass
import typing

from safebag import ChainProxy, chain, get_value


def assert_data_proxy(obj):
    assert type(obj) == ChainProxy


def test__not_nested__is_proxy():
    @dataclass
    class A:
        a: int
        b: typing.Optional[str] = None

    test_obj = A(1)
    test_obj_proxy = chain(test_obj)

    assert_data_proxy(test_obj_proxy.a)
    assert_data_proxy(test_obj_proxy.b)


def test__not_nested__values():
    @dataclass
    class A:
        a: int
        b: typing.Optional[str] = None

    test_obj = A(1)
    test_obj_proxy = chain(test_obj)

    assert get_value(test_obj_proxy.a) == 1
    assert get_value(test_obj_proxy.b) is None


def test__not_nested__false_nested():
    @dataclass
    class A:
        a: int
        b: typing.Optional[str] = None

    test_obj = A(1)
    test_obj_proxy = chain(test_obj)

    assert get_value(test_obj_proxy.a.not_existed) is None
    assert get_value(test_obj_proxy.b.not_existed) is None


def test__not_nested__bool_cast():
    @dataclass
    class A:
        a: int
        b: typing.Optional[str] = None

    test_obj = A(1)
    test_obj_proxy = chain(test_obj)

    assert bool(test_obj_proxy.a) is True
    assert bool(test_obj_proxy.b) is False
    assert bool(test_obj_proxy.b.not_existed) is False


def test__not_nested__bool_cast_full():
    @dataclass
    class A:
        a: int
        b: typing.Optional[str] = None

    test_obj = A(1, "test")
    test_obj_proxy = chain(test_obj)

    assert bool(test_obj_proxy.a) is True
    assert bool(test_obj_proxy.b) is True
    assert bool(test_obj_proxy.b.not_existed) is False


def test__nested__is_proxy():
    @dataclass
    class B:
        c: typing.Optional[str] = None

    @dataclass
    class A:
        a: int
        b: typing.Optional[B] = None

    test_obj = A(1, B("test"))
    test_obj_proxy = chain(test_obj)

    assert_data_proxy(test_obj_proxy.a)
    assert_data_proxy(test_obj_proxy.b)
    assert_data_proxy(test_obj_proxy.b.c)


def test__nested__values():
    @dataclass
    class B:
        c: typing.Optional[str] = None

    @dataclass
    class A:
        a: int
        b: typing.Optional[B] = None

    test_nested_obj = B("test")
    test_obj = A(1, test_nested_obj)
    test_obj_proxy = chain(test_obj)

    assert get_value(test_obj_proxy.a) == 1
    assert get_value(test_obj_proxy.b) == test_nested_obj
    assert get_value(test_obj_proxy.b.c) == "test"


def test__nested__bool_cast():
    @dataclass
    class B:
        c: typing.Optional[str] = None

    @dataclass
    class A:
        a: int
        b: typing.Optional[B] = None

    test_nested_obj = B("test")
    test_obj = A(1, test_nested_obj)
    test_obj_proxy = chain(test_obj)

    assert bool(test_obj_proxy.a) is True
    assert bool(test_obj_proxy.b) is True
    assert bool(test_obj_proxy.b.c) is True
    assert bool(test_obj_proxy.b.c.not_exist) is False
