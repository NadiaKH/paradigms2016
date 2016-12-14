class WritePurifier:
    def __init__(self):
        pass  
    def visit(self, tree):
        if tree is not None:
            return tree.accept(self)
        return 0                    #?

    def visitFuncCall(self, funccall):
        return self.visit(funccall.fun_expr)

    def visitFuncDef(self, funcdef):
        return self.visit(funcdef.function)
        
    def visitFunction(self, func):
        is_print = 0
        body = []
        for elem in func.body or []:
            if (is_print == 0):
                is_print = self.visit(elem)
                body.append(elem)
            else:
                break
        if (is_print == -1):
            elem = body.pop()
            if elem.__class__.__name__ == "Print":
                body.append(elem.expr)
            else:
                body.append(elem)
            func.body = body
            return -1
        return 0
            
        
    def visitCond(self, cond):
        is_print = 0
        if_true = []
        for elem in cond.if_true or []:
            if (is_print == 0):
                is_print = self.visit(elem)
                if_true.append(elem)
            else:
                break
        if (is_print == -1):
            elem = if_true.pop()
            if elem.__class__.__name__ == "Print":
                if_true.append(elem.expr)
            else:
                if_true.append(elem)
            cond.if_true = if_true
            return -1
        if_false = []
        for elem in cond.if_false or []:
            if (is_print == 0):
                is_print = self.visit(elem)
                if_false.append(elem)
            else:
                break
        if (is_print == -1):
            elem = if_false.pop()
            if elem.__class__.__name__ == "Print":
                if_false.append(elem.expr)
            else:
                if_true.append(elem)
            cond.if_false = if_false
            return -1
        return 0

    def visitPrint(self, prnt):
        return -1

    def visitNumber(self, num):
        return 0

    def visitBinOp(self, binop):
        return 0

    def visitUnOp(self, unop):
        return 0

    def visitReference(self, ref):
        return 0
        
class Scope:

    def __init__(self, parent = None):
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

    def accept(self, visitor):
        return visitor.visitNumber(self)


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = None
        for elem in self.body:
            res = elem.evaluate(scope)
        return res

    def accept(self, visitor):
        return visitor.visitFunction(self)


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visitFuncDef(self)


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

    def accept(self, visitor):
        return visitor.visitCond(self)
        

class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        number = self.expr.evaluate(scope)
        print(number.value)
        return number

    def accept(self, visitor):
        return visitor.visitPrint(self)


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

    def accept(self, visitor):
        return visitor.visitFuncCall(self)


class Reference:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visitReference(self)


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

    def accept(self, visitor):
        return visitor.visitBinOp(self)


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

    def accept(self, visitor):
        return visitor.visitUnOp(self)

def testCond():
    parent = Scope()
    WP = WritePurifier()
    cond = Conditional(Number(1), [Print(Number(5)), Number(5), Number(6)],
                                  [Print(Number(6))])
    WP.visit(cond)
    cond.evaluate(parent)
    counter = 0
    for elem in cond.if_true:
        counter+=1
    assert counter == 1
    assert cond.evaluate(parent).value == 5
    cond = Conditional(Number(1), [Conditional(Number(1), [Print(Number(7))])])
    WP.visit(cond)
    assert cond.evaluate(parent).value == 7

def testFunc():
    parent = Scope()
    WP = WritePurifier()
    prog = Conditional(Number(1), [
    FunctionDefinition('fac', Function(['n', 'cur'], [
    Conditional(
        BinaryOperation(Reference('n'), '==', Number(0)
    ), [
      Reference('cur')
    ], [
      BinaryOperation(Number(1), '+',
        FunctionCall(Reference('fac'), [
          BinaryOperation(Reference('n'), '-', Number(1)),
          BinaryOperation(Reference('cur'), '*', Reference('n')),
        ])
      )
    ])
    ])),
    FunctionCall(Reference('fac'), [Number(5), Number(1)])
    ])
    print(prog.evaluate(parent).value)
    WP.visit(prog)
    print(prog.evaluate(parent))

def otherTestFunc():
    parent = Scope()
    WP = WritePurifier()
    F = Function((), [Print(Number(10))])
    FD = FunctionDefinition("foo", F)
    FC = FunctionCall(FD, [])
    print(FC.evaluate(parent))
    WP.visit(FC)
    print(FC.evaluate(parent))

    F = Function(('a'), [Reference('a')])
    FD = FunctionDefinition("foo", F)
    FC = FunctionCall(FD, [Number(4)])
    print(FC.evaluate(parent).value)
    WP.visit(FC)
    print(FC.evaluate(parent).value)


if __name__ == "__main__":
    testCond()
    testFunc()
   # otherTestFunc()
