from rply.token import BaseBox
from interpreter.errors import *


# All token types inherit rply's basebox as rpython needs this
# These classes represent our Abstract Syntax Tree
# TODO: deprecate eval() as we move to compiling and then interpreting

class Variable(BaseBox):
    def __init__(self, name):
        self.name = str(name)
        self.value = None

    def get_name(self):
        return str(self.name)

    def eval(self, env):
        if env.variables.get(self.name, None) is not None:
            self.value = env.variables[self.name].eval(env)
            return self.value
        raise LogicError("Not yet defined")

    def to_string(self):
        return str(self.name)

    def rep(self):
        return 'Variable(%s)' % self.name


class Boolean(BaseBox):
    def __init__(self, value):
        if ["true", "false", "True", "False", "TRUE", "FALSE", ].__contains__(value):
            if value.lower().__eq__("true"):
                self.value = True
            if value.lower().__eq__("false"):
                self.value = False
        else:
            raise TypeError("Cannot cast boolean value while initiating Constant !")

    def eval(self):
        return self.value

    def rep(self):
        return 'Boolean(%s)' % self.value


class Integer(BaseBox):
    def __init__(self, value):
        self.value = int(value)

    def eval(self):
        return self.value

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'Integer(%s)' % self.value


class Float(BaseBox):
    def __init__(self, value):
        self.value = float(value)

    def eval(self):
        return self.value

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'Float(%s)' % self.value


class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def eval(self):
        return self.value

    def to_string(self):
        return '"%s"' % str(self.value)

    def rep(self):
        return 'String("%s")' % self.value


class Number:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right


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
    def __init__(self, value):
        self.value = value

    def eval(self):
        result = self.value.eval()
        if isinstance(result, bool):
            return not bool(result)
        raise LogicError("Cannot 'not' that")


class If(BaseBox):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

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
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self):
        print("Block statement's counter: %s" % len(self.statements))
        result = None
        for statement in self.statements:
            result = statement.eval()
            # print(result.to_string())
        return result

    def rep(self):
        result = 'Block('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class Print:
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())
