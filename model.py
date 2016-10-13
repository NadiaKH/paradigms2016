class Scope:

    def __init__(self, parent=None):
        self.parent = parent
        self.d = {}

    def __getitem__(self, name):
        if name not in self.d:
            return self.parent[name]
        else:
            return self.d[name]

    def __setitem__(self, name, value):
        self.d[name] = value


class Number:

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = None
        for elem in self.body:
            res = elem.evaluate(scope)
        return res


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    def __init__(self, condition, if_true, if_false=None):

        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        res = None
        if self.condition.evaluate(scope).value:
            for elem in self.if_true or []:
                res = elem.evaluate(scope)
        else:
            for elem in self.if_false or []:
                res = elem.evaluate(scope)
        return res


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        number = self.expr.evaluate(scope)
        print(number.value)
        return number


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        number = int(input())
        scope[self.name] = Number(number)
        return Number(number)


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        localscope = Scope(scope)
        function = self.fun_expr.evaluate(scope)
        for name, value in zip(function.args, self.args):
            localscope[name] = value.evaluate(scope)
        return function.evaluate(localscope)


class Reference:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope).value
        right = self.rhs.evaluate(scope).value
        if self.op == "+":
            return Number(left + right)
        elif self.op == "-":
            return Number(left - right)
        elif self.op == "*":
            return Number(left * right)
        elif self.op == "/":
            return Number(left // right)
        elif self.op == "%":
            return Number(left % right)
        elif self.op == "==":
            return Number(int(left == right))
        elif self.op == "!=":
            return Number(int(left != right))
        elif self.op == ">":
            return Number(int(left > right))
        elif self.op == "<":
            return Number(int(left < right))
        elif self.op == ">=":
            return Number(int(left >= right))
        elif self.op == "<=":
            return Number(int(left <= right))
        elif self.op == "&&":
            return Number(int(bool(left and right)))
        elif self.op == "||":
            return Number(int(bool(left or right)))


class UnaryOperation:

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        number = self.expr.evaluate(scope).value
        if self.op == "-":
            return Number(-number)
        elif self.op == "!":
            return Number(not number)


def testBinOper_1():
    parent = Scope()
    A = Number(5)
    B = Number(-5)
    C = Number(0)
    assert 0 == BinaryOperation(A, '+', B).evaluate(parent).value
    assert 10 == UnaryOperation(
        '-', (BinaryOperation(B, '-', A))).evaluate(parent).value
    assert -25 == BinaryOperation(A, '*', B).evaluate(parent).value
    assert -1 == BinaryOperation(A, '/', B).evaluate(parent).value
    assert 0 == BinaryOperation(A, '%', B).evaluate(parent).value
    assert 1 == BinaryOperation(A, '==',
                                UnaryOperation('-', B)).evaluate(parent).value
    assert 1 == BinaryOperation(A, '!=', B).evaluate(parent).value
    assert 1 == BinaryOperation(A, '>', B).evaluate(parent).value
    assert 0 == BinaryOperation(A, '<', B).evaluate(parent).value
    assert 1 == BinaryOperation(BinaryOperation(A, '+', B),
                                '>=',
                                C).evaluate(parent).value
    assert 0 == BinaryOperation(A, '<=', B).evaluate(parent).value
    assert 0 == BinaryOperation(BinaryOperation(A, '+', B),
                                '&&',
                                B).evaluate(parent).value
    assert 1 == BinaryOperation(C, '||', B).evaluate(parent).value


def testBinOper_2():
    parent = Scope()
    parent['N'] = BinaryOperation(Number(6), '+', Number(5)).evaluate(parent)
    assert 11 == Reference('N').evaluate(parent).value


def testBinOper_3():
    parent = Scope()
    parent['N'] = BinaryOperation(
        Number(6),
        '+',
        BinaryOperation(
            Number(7),
            '>',
            Number(8))).evaluate(parent)
    assert 6 == Reference('N').evaluate(parent).value


def testUnaryOper_1():
    parent = Scope()
    N = Number(10)
    assert -10 == UnaryOperation('-', Number(10)).evaluate(parent).value
    assert 0 == UnaryOperation('!', N).evaluate(parent).value


def testCond_1():
    parent = Scope()
    BinOp_1 = BinaryOperation(Reference('a'), '>', Reference('b'))
    BinOp_2 = BinaryOperation(Reference('a'), '<', Reference('b'))
    BinOp_3 = BinaryOperation(Reference('a'), '>=', Reference('b'))
    BinOp_4 = BinaryOperation(Reference('a'), '<=', Reference('b'))
    BinOp_5 = BinaryOperation(Reference('a'), '&&', Reference('b'))
    BinOp_6 = BinaryOperation(Reference('a'), '||', Reference('b'))
    UnOp_1 = UnaryOperation('!', Reference('a'))
    F1 = FunctionDefinition('F1',
                            Function(('a', 'b'),
                                     [BinOp_1]))
    C = Conditional(FunctionCall(F1, [Number(5), Number(3)]),
                    [Print(Number(1))],
                    [Print(Number(0))])
    assert 1 == C.evaluate(parent).value


def testCond_2():
    parent = Scope()
    F = FunctionCall(FunctionDefinition('F',
                                        Function((), [Print(Number(2))])),
                     [])
    cond = Conditional(BinaryOperation(Number(3), '>', Number(5)), [F])
    assert cond.evaluate(parent) is None


def testCond_3():
    parent = Scope()
    BinOp = BinaryOperation(Number(5), '>', Number(3))
    BinOp_2 = BinaryOperation(Reference('a'), '+', Reference('b'))
    F1 = FunctionDefinition('F1', Function(('a', 'b'), [Print(BinOp_2)]))
    F2 = FunctionDefinition('F2', Function(('a', 'b'), [Print(BinOp_2)]))
    Cond = Conditional(BinOp, [FunctionCall(F1, (Number(5), Number(6)))],
                       [FunctionCall(F2, [Number(3), Number(2)])])
    assert 11 == Cond.evaluate(parent).value


def testCond_4():
    parent = Scope()
    BinOp_or = BinaryOperation(Reference('a'), '||', Reference('b'))
    parent['a'] = Number(1)
    parent['b'] = Number(0)
    BinOp_and = BinaryOperation(Reference('a'), '&&', Reference('b'))
    assert 0 == Print(BinOp_and).evaluate(parent).value
    assert 1 == Print(BinOp_or).evaluate(parent).value
    Cond_2 = Conditional(
        Number(0), [
            Print(
                Reference('a'))], [
            Print(
                Reference('b'))])
    Cond_1 = Conditional(BinOp_or, [Cond_2], [Print(Number(1000))])
    assert 0 == Cond_1.evaluate(parent).value


def testCond_5():
    parent = Scope()
    cond = Conditional(BinaryOperation(Number(3), '>', Number(5)),
                       [Print(Number(3))],
                       [Print(Number(5))])
    assert 5 == cond.evaluate(parent).value


def testReference_1():
    grand = Scope()
    parent = Scope(grand)
    child = Scope(parent)
    grand['a'] = Number(1)
    grand['b'] = Number(0)
    parent['c'] = Number(2)
    assert 1 == Print(Reference('a')).evaluate(grand).value
    assert 0 == Print(Reference('b')).evaluate(grand).value
    assert 1 == Print(Reference('a')).evaluate(parent).value
    assert 0 == Print(Reference('b')).evaluate(child).value
    assert 2 == Print(Reference('c')).evaluate(child).value


def testPrint_1():
    parent = Scope()
    N = Number(10)
    P = Print(N)
    P.evaluate(parent)
    assert 5 == Print(Number(5)).evaluate(parent).value


def testPrint_2():
    parent = Scope()
    parent['a'] = Number(0)
    assert 0 == Print(Reference('a')).evaluate(parent).value


def testFunc_1():
    parent = Scope()
    F = Function(('a', 'b'),
                 [Print(BinaryOperation(Reference('a'),
                                        '+',
                                        Reference('b')))])
    FuncDef_1 = FunctionDefinition('foo_1', F)
    assert 5 == FunctionCall(
        FuncDef_1, [
            Number(2), Number(3)]).evaluate(parent).value


def testFunc_2():
    parent = Scope()
    F = Function(('a', 'b'), [Print(BinaryOperation(Reference('a'),
                                                    '+',
                                                    Reference('b')))])
    G = Function(('a', 'b'), [BinaryOperation(Reference('a'),
                                              '*',
                                              Reference('b'))])
    FuncDef_F = FunctionDefinition('foo_F', F)
    FuncDef_G = FunctionDefinition('foo_G', G)
    FC = FunctionCall(FuncDef_G, [Number(1), Number(2)])
    assert 7 == FunctionCall(FuncDef_F, [FC, Number(5)]).evaluate(parent).value


def testFunc_3():
    parent = Scope()
    BinOp = BinaryOperation(Reference('a'), '+', Reference('b'))
    parent['foo'] = Function(('a', 'b'), [Print(BinOp)])
    FuncDef = FunctionDefinition('foo', parent['foo'])
    assert 5 == FunctionCall(
        FuncDef, [
            Number(2), Number(3)]).evaluate(parent).value


def testFunc_4():
    parent = Scope()
    assert 10 == Print(Number(10)).evaluate(parent).value
    F = Function((), [Print(Number(10))])
    FunctionCall(FunctionDefinition('F', F), []).evaluate(parent)


def testFunc_5():
    parent = Scope()
    F = Function((), [Print(Number(10))])
    FuncDef = FunctionDefinition('foo', F)
    assert 10 == FunctionCall(FuncDef, []).evaluate(parent).value


def testFunc_6():
    parent = Scope()
    BinOpInc = BinaryOperation(Reference('a'), '+', Number(1))
    F = FunctionDefinition('F', Function(('a', 'b'), [BinOpInc]))
    assert 6 == FunctionCall(F, [Number(5)]).evaluate(parent).value


def testFunc_7():
    parent = Scope()
    BinOpInc = BinaryOperation(Reference('a'), '+', Number(1))
    F = FunctionDefinition('F', Function(('a'), [BinOpInc]))
    assert 5 == FunctionCall(F, [Number(4)]).evaluate(parent).value


def testCond_6():
    parent = Scope()
    cond = Conditional(Number(1), [], [])
    assert cond.evaluate(parent) is None


def testCond_7():
    parent = Scope()
    cond = Conditional(Number(0), [], [])
    assert cond.evaluate(parent) is None


def testCond_8():
    parent = Scope()
    cond = Conditional(Number(1), None, [])
    assert cond.evaluate(parent)is None


def testRead_1():
    parent = Scope()
    print("input number 5")
    R = Read('N').evaluate(parent)
    assert 5 == R.value


def testScope_1():
    parent = Scope()
    parent['a'] = Number(5)
    assert 'a' in parent.d


def testScope_2():
    parent = Scope()
    FD = FunctionDefinition('foo', Function(('a'), [Reference('a')]))
    FunctionCall(FD, [Number(4)]).evaluate(parent)
    assert 'a' not in parent.d


def testFuncCall_1():
    parent = Scope()
    F = Function(('a', 'b'), [Reference('a'), Reference('b')])
    FD = FunctionDefinition('foo', F)
    FC = FunctionCall(FD, [Number(4), Number(5)])
    FC.evaluate(parent)
    assert 'a' not in parent.d
    assert 'b' not in parent.d

if __name__ == '__main__':
    testBinOper_1()
    testBinOper_2()
    testBinOper_3()
    testUnaryOper_1()
    testCond_1()
    testCond_2()
    testCond_3()
    testCond_4()
    testCond_5()
    testCond_6()
    testCond_7()
    testCond_8()
    testReference_1()
    testPrint_1()
    testPrint_2()
    testFunc_1()
    testFunc_2()
    testFunc_3()
    testFunc_4()
    testFunc_5()
    testFunc_6()
    testFunc_7()
    testScope_1()
    testScope_2()
    testFuncCall_1()
    testRead_1()
