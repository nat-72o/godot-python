import pytest

from godot.bindings import Environment, Node
from godot import RID


class TestRID:
    def test_base(self):
        v = RID()
        assert type(v) == RID

    def test_equal(self):
        v1 = RID()
        v2 = RID()
        assert v1 == v2
        # Environment is a Ressource which provides unique rid per instance
        res_a = Environment()
        v_a_1 = RID(res_a)
        assert v_a_1 != v1
        v_a_2 = RID(res_a)
        assert v_a_1 == v_a_2
        res_b = Environment()
        v_b = RID(res_b)
        assert not v_a_1 == v_b  # Force use of __eq__

    @pytest.mark.parametrize("arg", [None, 0, "foo"])
    def test_bad_equal(self, arg):
        arr = RID(Environment())
        assert arr != arg

    def test_bad_equal_with_rid(self):
        # Doing `RID(Environment())` will cause garbage collection of enclosed
        # Environment object and possible reuse of it id
        env1 = Environment()
        env2 = Environment()
        rid1 = RID(env1)
        rid2 = RID(env2)
        assert rid1 != rid2

    def test_repr(self):
        v = RID()
        assert repr(v) == "<RID(id=0)>"

    @pytest.mark.parametrize(
        "arg", [42, "dummy", Node(), RID()]  # Node doesn't inherit from Resource
    )
    def test_bad_instantiate(self, arg):
        with pytest.raises(TypeError):
            RID(arg)

    @pytest.mark.parametrize("args", [["get_id", int, ()]], ids=lambda x: x[0])
    def test_methods(self, args):
        v = RID()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type


# @pytest.mark.parametrize('args', [
#     (Vector2(0, 0), Vector2(2, 3)),
#     (Vector2(3, 2), Vector2(-1, 1)),
#     (Vector2(-1, -1), Vector2(3, 4)),
# ], ids=lambda x: x[0])
# def test_lt(self, args):
#     param, result = args
#     calc = Vector2(2, 3) - param
#     assert calc == result

# @pytest.mark.parametrize('arg', [
#     None, 1, 'dummy'
# ], ids=lambda x: x[0])
# def test_bad_add(self, arg):
#     with pytest.raises(TypeError):
#         Vector2(2, 3) + arg
