from rply.token import BaseBox
from compiler.errors import *


# All token types inherit rply's basebox as rpython needs this
# These classes represent our Abstract Syntax Tree
# TODO: deprecate eval(env) as we move to compiling and then interpreting

class Variable(BaseBox):
    def __init__(self, name, state):
        self.name = str(name)
        self.value = None
        self.env = state

    def get_name(self):
        return str(self.name)

    def eval(self):
        if dict(self.env.variables).get(self.name) is not None:
            self.value = self.env.variables[self.name].eval()
            return self.value
        raise LogicError("Variable <%s> is not yet defined" % str(self.name))

    def to_string(self):
        return str(self.name)

    def rep(self):
        return 'Variable(%s)' % self.name


class BaseFunction(BaseBox):
    def __init__(self, expression, state):
        self.value = expression.eval()
        self.env = state

    def eval(self):
        return self.value

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'BaseFunction(%s)' % self.value


class Absolute(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)
        import re as regex
        self.match = regex.search('^-?\d+(\.\d+)?$', str(self.value))
        if self.match:
            self.value = abs(self.value)
        else:
            raise ValueError("Cannot abs() not numerical values !")

    def rep(self):
        return 'Absolute(%s)' % self.value


class Sin(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)
        import re as regex
        self.match = regex.search('^-?\d+(\.\d+)?$', str(self.value))
        if self.match:
            import math
            self.value = math.sin(self.value)
        else:
            raise ValueError("Cannot sin() not numerical values !")

    def rep(self):
        return 'Sin(%s)' % self.value


class Cos(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)
        import re as regex
        self.match = regex.search('^-?\d+(\.\d+)?$', str(self.value))
        if self.match:
            import math
            self.value = math.cos(self.value)
        else:
            raise ValueError("Cannot cos() not numerical values !")

    def rep(self):
        return 'Cos(%s)' % self.value


class Tan(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)
        import re as regex
        self.match = regex.search('^-?\d+(\.\d+)?$', str(self.value))
        if self.match:
            import math
            self.value = math.tan(self.value)
        else:
            raise ValueError("Cannot tan() not numerical values !")

    def rep(self):
        return 'Tan(%s)' % self.value


class Pow(BaseFunction):
    def __init__(self, expression, expression2, state):
        super().__init__(expression, state)
        self.value2 = expression2.eval()
        import re as regex
        self.match = regex.search('^-?\d+(\.\d+)?$', str(self.value))
        self.match2 = regex.search('^-?\d+(\.\d+)?$', str(self.value2))
        if self.match and self.match2:
            import math
            self.value = math.pow(self.value, self.value2)
        else:
            raise ValueError("Cannot pow() not numerical values !")

    def rep(self):
        return 'Pow(%s)' % self.value


# ABSTRACT CLASS! DO NOT USE!
class Constant(BaseBox):
    def __init__(self, state):
        self.value = None
        self.env = state

    def eval(self):
        return self.value

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'Constant(%s)' % self.value


class Boolean(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        if ["true", "false", "True", "False", "TRUE", "FALSE", ].__contains__(value):
            if value.lower().__eq__("true"):
                self.value = True
            if value.lower().__eq__("false"):
                self.value = False
        else:
            raise TypeError("Cannot cast boolean value while initiating Constant !")

    def rep(self):
        return 'Boolean(%s)' % self.value


class Integer(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = int(value)

    def rep(self):
        return 'Integer(%s)' % self.value


class Float(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = float(value)

    def rep(self):
        return 'Float(%s)' % self.value


class String(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = str(value)

    def to_string(self):
        return '"%s"' % str(self.value)

    def rep(self):
        return 'String("%s")' % self.value


class ConstantPI(Constant):
    def __init__(self, name, state):
        super().__init__(state)
        import math
        self.name = str(name)
        if str(name).__contains__('-'):
            self.value = float(-math.pi)
        else:
            self.value = float(math.pi)

    def rep(self):
        return '%s(%f)' % (self.name, self.value)


class ConstantE(Constant):
    def __init__(self, name, state):
        super().__init__(state)
        import math
        self.name = str(name)
        if str(name).__contains__('-'):
            self.value = float(-math.pi)
        else:
            self.value = float(math.pi)

    def rep(self):
        return '%s(%f)' % (self.name, self.value)


class BinaryOp(BaseBox):
    def __init__(self, left, right, state):
        self.left = left
        self.right = right
        self.env = state


class Assignment(BinaryOp):
    def eval(self):
        if isinstance(self.left, Variable):
            var_name = self.left.get_name()
            if dict(self.env.variables).get(var_name) is None:
                self.env.variables[var_name] = self.right.eval()
                print(self.env.variables)
                return self.env.variables  # Return the ParserState() that hold the variables.

            # Otherwise raise error
            raise ImmutableError(var_name)

        else:
            raise LogicError("Cannot assign to <%s>" % self)

    def rep(self):
        return 'Assignment(%s, %s)' % (self.left.rep(), self.right.rep())


class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()


class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()


class Equal(BinaryOp):
    def eval(self):
        return self.left.eval() == self.right.eval()


class NotEqual(BinaryOp):
    def eval(self):
        return self.left.eval() != self.right.eval()


class GreaterThan(BinaryOp):
    def eval(self):
        return self.left.eval() > self.right.eval()


class LessThan(BinaryOp):
    def eval(self):
        return self.left.eval() < self.right.eval()


class GreaterThanEqual(BinaryOp):
    def eval(self):
        return self.left.eval() >= self.right.eval()


class LessThanEqual(BinaryOp):
    def eval(self):
        return self.left.eval() <= self.right.eval()


class And(BinaryOp):
    def eval(self):
        return self.left.eval() and self.right.eval()


class Or(BinaryOp):
    def eval(self):
        return self.left.eval() or self.right.eval()


class Not(BaseBox):
    def __init__(self, expression, state):
        self.value = expression.eval()
        self.env = state

    def eval(self):
        if isinstance(self.value, bool):
            return not bool(self.value)
        raise LogicError("Cannot 'not' that")


class If(BaseBox):
    def __init__(self, condition, body, else_body=None, state=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.env = state

    def eval(self):
        condition = self.condition.eval()
        if bool(condition) is True:
            return self.body.eval()
        else:
            if self.else_body is not None:
                return self.else_body.eval()
        return None

    def rep(self):
        return 'If(%s) Then(%s) Else(%s)' % (self.condition.rep(), self.body.rep(), self.else_body.rep())


class Block(BaseBox):
    def __init__(self, statement, block, state):
        self.env = state
        if type(block) is Block:
            self.statements = block.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self):
        print("Block statement's counter: %s" % len(self.statements))
        result = None
        for statement in self.statements:
            result = statement.eval()  # Only now the statement.eval() does effect !
            # print(result.to_string())
        return result  # The result is not been used yet !

    def rep(self):
        result = 'Block('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class Print:
    def __init__(self, expression, state):
        self.value = expression.eval()
        self.env = state

    def eval(self):
        print(self.value)
