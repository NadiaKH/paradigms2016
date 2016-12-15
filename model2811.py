class WritePurifier:
    def __init__(self):
        pass  
    def visit(self, tree):
        if tree is not None:
            return tree.accept(self)
        return None                #?

    def visitFuncCall(self, funccall):
        funccall.fun_expr = self.visit(funccall.fun_expr)
        return  funccall

    def visitFuncDef(self, funcdef):
        funcdef.function = self.visit(funcdef.function)
        return funcdef        

    def visitFunction(self, func):
        body = []
        for elem in reversed(func.body):
            elem = self.visit(elem)
            body = [Conditional((BinaryOperation(elem,
                                                '>',
                                                Number(0))),
                               body.insert(0, elem),
                               [UnaryOperation('-', elem)])]
        func.body = body
        return func
            
        
    def visitCond(self, cond):  
        if_true = []
        if_false = []
        for elem in reversed(cond.if_true or []):
            elem = self.visit(elem)
            if_true = [Conditional((BinaryOperation(elem,
                                                   '>',
                                                   Number(0))),
                                   if_true.insert(0, elem),
                                   [UnaryOperation('-', elem)])]
        
        for elem in reversed(cond.if_false  or []):
            elem = self.visit(elem)
            if_false = [Conditional((BinaryOperation(elem,
                                                    '>',
                                                    Number(0))),
                                    if_false.insert(0, elem),
                                    [UnaryOperation('-', elem)])]
        cond.if_false = if_false
        cond.if_true = if_true
        return cond

    def visitPrint(self, prnt):
        return UnaryOperation('-', prnt.expr)

    def visitNumber(self, num):
        return num

    def visitBinOp(self, binop):
        lhs = []
        rhs = []
        for elem in reversed(binop.lhs):
            elem = self.visit(elem)
            lhs = [Conditional((BinaryOperation(elem,
                                              '>',
                                              Number(0))),
                              lhs.insert(0, elem),
                              [UnaryOperation('-', elem)])]
        for elem in reversed(binop.rhs):
            elem = self.visit(elem)
            rhs = [Conditional((BinaryOperation(elem,
                                              '>',
                                              Number(0))),
                              rhs.insert(0, elem),
                              [UnaryOperation('-', elem)])]
        binop.lhs = lhs
        binop.rhs = rhs
        return binop

    def visitUnOp(self, unop):
        expr = []
        for elem in reversed(unop.expr):
            elem = self.visit(elem)
            expr = [Consitional((BinaryOperation(elem,
                                                '>',
                                                Number(0))),
                               expr.insert(0, elem),
                               [UnaryOperation('-', elem)])]
        unop.expr = expr
        return unop

    def visitReference(self, ref):
        return ref
        
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
    cond1 = Conditional(Number(1), [Print(Number(7))])
    cond = Conditional(Number(1),[cond1])
    WP.visit(cond)
    #for x in cond.if_true:
    #    print(x.__class__.__name__)
    #    print(x.condition.__class__.__name__)
    #    print(x.condition.evaluate(parent).value)
    #    print(x.if_true)
    #cond.evaluate(parent)
    #print(cond.evaluate(parent))
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
    #print(prog.evaluate(parent).value)
    WP.visit(prog)
    #print(prog.evaluate(parent))

def testFunc2():
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
    prog.evaluate(parent)
    #print(prog.evaluate(parent).value)
    #WP.visit(prog)
    #print(prog.evaluate(parent))

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

def testV0():
    parent = Scope()
    WP = WritePurifier()
    p = Print(Number(5))
    f = WP.visit(p)
    assert -5 == f.evaluate(parent).value

def testV1():
    parent = Scope()
    WP = WritePurifier()
    cond = Conditional((Number(1)),
                       [Print(Number(2))], [Number(5)])
    c = WP.visit(cond)
    assert 2 == cond.evaluate(parent).value
    assert 2 == c.evaluate(parent).value

def testV2():
    parent = Scope()
    WP = WritePurifier()
    f = Function((), [Print(Number(10))])
    WP.visit(f)
    assert 10 == f.evaluate(parent).value

if __name__ == "__main__":
    testV0()
    testV1()
    testV2()
    testCond()
    testFunc2()
   # otherTestFunc()
