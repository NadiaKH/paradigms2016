import sys
import io
from model import *
from io import StringIO


def get_v(n):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    Print(n).evaluate(Scope())
    res = int(sys.stdout.getvalue())
    sys.stdout = old_stdout
    return res


        
class TestRead:

    def test_simple(self, monkeypatch):
        monkeypatch.setattr(sys, "stdin", StringIO('6'))
        assert get_v(Read('a')) == 6


class TestPrint:
    
    def test_simple(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        Print(Number(10)).evaluate({})
        assert int(sys.stdout.getvalue()) == 10

    def test_print_number(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        Print(Number(10)).evaluate(scope)
        assert int(sys.stdout.getvalue()) == 10

    def test_print_reference(self, monkeypatch):
        parent = {}
        parent['a'] = Number(-10)
        monkeypatch.setattr(sys, "stdout", StringIO())
        Print(Reference('a')).evaluate(parent)
        assert int(sys.stdout.getvalue()) == -10


class TestNumber:

    def test_simple(self):
        assert get_v(Number(-10)) == -10


class TestScope:

    def test_number(self):
        parent = Scope()
        num = Number(0)
        parent['num'] = num
        assert parent['num'] is num

    def test_parent(self):
        parent = Scope()
        foo = Function([], [])
        parent['foo'] = foo
        scope = Scope(parent)
        assert scope['foo'] is foo


class TestReference:

    def test_simple(self):
        scope = {}
        scope['a'] = Number(5)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        Print(Reference('a')).evaluate(scope)
        assert int(sys.stdout.getvalue()) == 5
        sys.stdout = old_stdout


class TestBinaryOperation:

    def test_plus(self):
        binop = BinaryOperation(Number(5), '+', Number(6))
        assert get_v(binop) == 11

    def test_minus(self):
        binop = BinaryOperation(Number(5), '-', Number(6))
        assert get_v(binop) == -1

    def test_multiply(self):
        binop = BinaryOperation(Number(5), '*', Number(6))
        assert get_v(binop) == 30

    def test_division(self):
        binop = BinaryOperation(Number(6), '/', Number(5))
        assert get_v(binop) == 1

    def test_mod(self):
        binop = BinaryOperation(Number(6), '%', Number(5))
        assert get_v(binop) == 1

    def test_eq(self):
        binop1 = BinaryOperation(Number(5), '==', Number(6))
        binop2 = BinaryOperation(Number(6), '==', Number(6))
        assert get_v(binop1) == 0
        assert get_v(binop2) != 0

    def test_not_eq(self):
        binop1 = BinaryOperation(Number(5), '!=', Number(6))
        binop2 = BinaryOperation(Number(6), '!=', Number(6))
        assert get_v(binop1) != 0
        assert get_v(binop2) == 0

    def test_great(self):
        binop1 = BinaryOperation(Number(5), '>', Number(6))
        binop2 = BinaryOperation(Number(6), '>', Number(6))
        binop3 = BinaryOperation(Number(6), '>', Number(5))
        assert get_v(binop1) == 0
        assert get_v(binop2) == 0
        assert get_v(binop3) != 0

    def test_less(self):
        binop1 = BinaryOperation(Number(5), '<', Number(6))
        binop2 = BinaryOperation(Number(6), '<', Number(6))
        binop3 = BinaryOperation(Number(6), '<', Number(5))
        assert get_v(binop1) != 0
        assert get_v(binop2) == 0
        assert get_v(binop3) == 0

    def test_great_or_eq(self):
        binop1 = BinaryOperation(Number(5), '>=', Number(6))
        binop2 = BinaryOperation(Number(6), '>=', Number(6))
        binop3 = BinaryOperation(Number(6), '>=', Number(5))
        assert get_v(binop1) == 0
        assert get_v(binop2) != 0
        assert get_v(binop3) != 0

    def test_less_or_eq(self):
        binop1 = BinaryOperation(Number(5), '<=', Number(6))
        binop2 = BinaryOperation(Number(6), '<=', Number(6))
        binop3 = BinaryOperation(Number(6), '<=', Number(5))
        assert get_v(binop1) != 0
        assert get_v(binop2) != 0
        assert get_v(binop3) == 0

    def test_and(self):
        binop1 = BinaryOperation(Number(1), '&&', Number(0))
        binop2 = BinaryOperation(Number(1), '&&', Number(1))
        binop3 = BinaryOperation(Number(0), '&&', Number(0))
        binop4 = BinaryOperation(Number(0), '&&', Number(1))
        assert get_v(binop1) == 0
        assert get_v(binop2) != 0
        assert get_v(binop3) == 0
        assert get_v(binop4) == 0

    def test_or(self):
        binop1 = BinaryOperation(Number(1), '||', Number(0))
        binop2 = BinaryOperation(Number(1), '||', Number(1))
        binop3 = BinaryOperation(Number(0), '||', Number(0))
        binop4 = BinaryOperation(Number(0), '||', Number(1))
        assert get_v(binop1) != 0
        assert get_v(binop2) != 0
        assert get_v(binop3) == 0
        assert get_v(binop4) != 0


class TestUnaryOperation:

    def test_minus(self):
        unop = UnaryOperation('-', Number(5))
        assert get_v(unop) == -5

    def test_negl_false(self):
        unop = UnaryOperation('!', Number(5))
        assert get_v(unop) == 0

    def test_negl_true(self):
        unop = UnaryOperation('!', Number(0))
        assert get_v(unop) != 0


class TestConditional:

    def test_simple(self):
        cond = Conditional((Number(1)), [Number(5)], [Number(6)])
        assert get_v(cond) == 5

    def test_empty_or_none(self):
        parent = Scope()
        Conditional((Number(1)), [], []).evaluate(parent)
        Conditional((Number(0)), [], []).evaluate(parent)
        Conditional((Number(1)), []).evaluate(parent)
        Conditional((Number(1)), []).evaluate(parent)
        Conditional((Number(0)), []).evaluate(parent)
        Conditional((Number(1)), None, None).evaluate(parent)
        Conditional((Number(0)), None).evaluate(parent)

    def test_condition_true(self):
        cond = Conditional((Number(5)), [Number(9), Number(10)], [Number(11)])
        assert get_v(cond) == 10

    def test_condition_false(self):
        cond = Conditional((Number(0)), [Number(10)], [Number(11), Number(12)])
        assert get_v(cond) == 12


class TestFunction:

    def test_simple(self):
        func = Function((), [Number(7)])
        assert get_v(func) == 7

    def test_empty(self):
        Function((), []).evaluate({})

    def test_none(self):
        Function((), None).evaluate({})


class TestFunctionDefinition:

    def test_simple(self):
        parent = {}
        func = Function((), [])
        funcdef = FunctionDefinition('F', func)
        assert func is funcdef.evaluate(parent)


class TestFunctionCall:

    def test_simple(self):
        parent = {}
        func = Function((), [Number(6)])
        funcdef = FunctionDefinition('F', func)
        funccall = FunctionCall(funcdef, [])
        assert get_v(funccall) == 6

    def test_args(self):
        parent = Scope()
        func = Function(('a', 'b'), [BinaryOperation(Reference('a'),
                                                  '+',
                                                  Reference('b'))])
        funcdef = FunctionDefinition('F', func)
        funccall = FunctionCall(funcdef, [Number(2), Number(3)])
        assert get_v(funccall) == 5


class IntegrationTest:

    def test_function_print(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        parent = Scope()
        func = Function(('a', 'b'),
                     [Print(BinaryOperation(Reference('a'),
                                            '+',
                                            Reference('b')))])
        funcdef = FunctionDefinition('F', func)
        FunctionCall(funcdef, [Number(2), Number(3)]).evaluate(parent)
        assert int(sys.stdout.getvalue()) == 5
        sys.stdout = old_stdout

    def test_function(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        parent = Scope()
        func = Function(('a'), [Print(Reference('a'))])
        funcdef = FunctionDefinition('foo', func)
        FunctionCall(funcdef, [Number(2)]).evaluate(parent)
        assert int(sys.stdout.getvalue()) == 2
