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
            
