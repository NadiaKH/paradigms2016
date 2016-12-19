import sys
import io
from model import *


def get_v(n):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    Print(n).evaluate(Scope())
    res = int(sys.stdout.getvalue())
    sys.stdout = old_stdout
    return res


class TestRead:

    def test_simple(self):
        old_stdin = sys.stdin
        sys.stdin = io.StringIO('6')
        assert get_v(Read('a')) == 6
        sys.stdin = old_stdin


class TestPrint:

    def test_print_number(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        scope = Scope()
        N = Number(10)
        Print(N).evaluate(scope)
        assert int(sys.stdout.getvalue()) == 10
        sys.stdout = old_stdout

    def test_print_reference(self):
        parent = {}
        parent['a'] = Number(-10)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        Print(Reference('a')).evaluate(parent)
        assert int(sys.stdout.getvalue()) == -10
        sys.stdout = old_stdout


class TestNumber:

    def test_simple(self):
        N = Number(-10)
        assert get_v(N) == -10


class TestScope:

    def test_number(self):
        parent = Scope()
        N = Number(0)
        parent['N'] = N
        assert parent['N'] is N

    def test_parent(self):
        parent = Scope()
        foo = Function([], [])
        parent['foo'] = foo
        scope = Scope(parent)
        assert scope['foo'] is foo

    def test_not_in_scope(self):
        parent = Scope()
        try:
            parent['a']
        except TypeError:
            pass


class TestReference:

    def test_scope(self):
        grand = Scope()
        parent = Scope(grand)
        child = Scope(parent)
        G = Number(60)
        P = Number(30)
        Ch = Number(6)
        grand['G'] = G
        parent['P'] = P
        child['Ch'] = Ch
        assert Ch is child['Ch']
        assert P is child['P']
        assert P is parent['P']
        assert G is child['G']
        assert G is parent['G']
        assert G is grand['G']

    def test_function(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        parent = Scope()
        F = Function(('a'), [Print(Reference('a'))])
        FD = FunctionDefinition('foo', F)
        FunctionCall(FD, [Number(2)]).evaluate(parent)
        assert int(sys.stdout.getvalue()) == 2


class TestBinaryOperation:

    def test_plus(self):
        BO = BinaryOperation(Number(5), '+', Number(6))
        assert get_v(BO) == 11

    def test_minus(self):
        BO = BinaryOperation(Number(5), '-', Number(6))
        assert get_v(BO) == -1

    def test_multiply(self):
        BO = BinaryOperation(Number(5), '*', Number(6))
        assert get_v(BO) == 30

    def test_division(self):
        BO = BinaryOperation(Number(6), '/', Number(5))
        assert get_v(BO) == 1

    def test_mod(self):
        BO = BinaryOperation(Number(6), '%', Number(5))
        assert get_v(BO) == 1

    def test_eq(self):
        BO1 = BinaryOperation(Number(5), '==', Number(6))
        BO2 = BinaryOperation(Number(6), '==', Number(6))
        assert get_v(BO1) == 0
        assert get_v(BO2) == 1

    def test_not_eq(self):
        BO1 = BinaryOperation(Number(5), '!=', Number(6))
        BO2 = BinaryOperation(Number(6), '!=', Number(6))
        assert get_v(BO1) == 1
        assert get_v(BO2) == 0

    def test_great(self):
        BO1 = BinaryOperation(Number(5), '>', Number(6))
        BO2 = BinaryOperation(Number(6), '>', Number(6))
        BO3 = BinaryOperation(Number(6), '>', Number(5))
        assert get_v(BO1) == 0
        assert get_v(BO2) == 0
        assert get_v(BO3) == 1

    def test_less(self):
        BO1 = BinaryOperation(Number(5), '<', Number(6))
        BO2 = BinaryOperation(Number(6), '<', Number(6))
        BO3 = BinaryOperation(Number(6), '<', Number(5))
        assert get_v(BO1) == 1
        assert get_v(BO2) == 0
        assert get_v(BO3) == 0

    def test_great_or_eq(self):
        BO1 = BinaryOperation(Number(5), '>=', Number(6))
        BO2 = BinaryOperation(Number(6), '>=', Number(6))
        BO3 = BinaryOperation(Number(6), '>=', Number(5))
        assert get_v(BO1) == 0
        assert get_v(BO2) == 1
        assert get_v(BO3) == 1

    def test_less_or_eq(self):
        BO1 = BinaryOperation(Number(5), '<=', Number(6))
        BO2 = BinaryOperation(Number(6), '<=', Number(6))
        BO3 = BinaryOperation(Number(6), '<=', Number(5))
        assert get_v(BO1) == 1
        assert get_v(BO2) == 1
        assert get_v(BO3) == 0

    def test_and(self):
        BO1 = BinaryOperation(Number(1), '&&', Number(0))
        BO2 = BinaryOperation(Number(1), '&&', Number(1))
        BO3 = BinaryOperation(Number(0), '&&', Number(0))
        BO4 = BinaryOperation(Number(0), '&&', Number(1))
        assert get_v(BO1) == 0
        assert get_v(BO2) == 1
        assert get_v(BO3) == 0
        assert get_v(BO4) == 0

    def test_or(self):
        BO1 = BinaryOperation(Number(1), '||', Number(0))
        BO2 = BinaryOperation(Number(1), '||', Number(1))
        BO3 = BinaryOperation(Number(0), '||', Number(0))
        BO4 = BinaryOperation(Number(0), '||', Number(1))
        assert get_v(BO1) == 1
        assert get_v(BO2) == 1
        assert get_v(BO3) == 0
        assert get_v(BO4) == 1


class TestUnaryOperation:

    def test_minus(self):
        UO = UnaryOperation('-', Number(5))
        assert get_v(UO) == -5

    def test_negl(self):
        UO = UnaryOperation('!', Number(5))
        assert get_v(UO) == 1


class TestConditional:

    def test_simple(self):
        C = Conditional((Number(1)), [Number(5)], [Number(6)])
        assert get_v(C) == 5

    def test_empty(self):
        parent = Scope()
        Conditional((Number(1)), [], []).evaluate(parent)
        Conditional((Number(0)), [], []).evaluate(parent)
        Conditional((Number(1)), []).evaluate(parent)

    def test_none(self):
        parent = Scope()
        Conditional((Number(1)), []).evaluate(parent)
        Conditional((Number(0)), []).evaluate(parent)
        Conditional((Number(1)), None, None).evaluate(parent)
        Conditional((Number(0)), None).evaluate(parent)


class TestFunction:

    def test_simple(self):
        F = Function((), [Number(7)])
        assert get_v(F) == 7

    def test_empty(self):
        parent = {}
        Function((), []).evaluate(parent)

    def test_none(self):
        parent = {}
        Function((), None).evaluate(parent)

    def test_fcall(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        parent = Scope()
        F = Function(('a', 'b'),
                     [Print(BinaryOperation(Reference('a'),
                                            '+',
                                            Reference('b')))])
        FD = FunctionDefinition('F', F)
        FunctionCall(FD, [Number(2), Number(3)]).evaluate(parent)
        assert int(sys.stdout.getvalue()) == 5
        sys.stdout = old_stdout


class TestFunctionDefinition:

    def test_simple(self):
        parent = {}
        F = Function((), [])
        FD = FunctionDefinition('F', F)
        assert F is FD.evaluate(parent)


class TestFunctionCall:

    def test_simple(self):
        parent = {}
        F = Function((), [Number(6)])
        FD = FunctionDefinition('F', F)
        FC = FunctionCall(FD, [])
        assert get_v(FC) == 6

    def test_args(self):
        parent = Scope()
        F = Function(('a', 'b'), [BinaryOperation(Reference('a'),
                                                  '+',
                                                  Reference('b'))])
        FD = FunctionDefinition('F', F)
        FC = FunctionCall(FD, [Number(2), Number(3)])
        assert get_v(FC) == 5
