from rply.token import BaseBox
from compiler.errors import *


# All token types inherit rply's basebox as rpython needs this
# These classes represent our Abstract Syntax Tree
# TODO: deprecate eval(env) as we move to compiling and then interpreting

class Program(BaseBox):
    def __init__(self, statement, program, state):
        self.env = state
        if type(program) is Program:
            self.statements = program.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self, env):
        # print("Program<%s> statement's counter: %s" % (self, len(self.statements)))
        result = None
        for statement in self.statements:
            result = statement.eval(env)  # Only now the statement.eval(env) does effect !
        return result  # The result is not been used yet !

    def rep(self):
        result = 'Program('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


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

    def eval(self, env):
        # print("Block<%s> statement's counter: %s" % (self, len(self.statements)))
        result = None
        for statement in self.statements:
            result = statement.eval(env)  # Only now the statement.eval(env) does effect !
        return result  # The result is not been used yet !

    def rep(self):
        result = 'Block('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class If(BaseBox):
    def __init__(self, condition, body, else_body=None, state=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.env = state

    def eval(self, env):
        condition = self.condition.eval(env)
        if bool(condition) is True:
            return self.body.eval(env)
        else:
            if self.else_body is not None:
                return self.else_body.eval(env)
        return None

    def rep(self):
        return 'If(%s) Then(%s) Else(%s)' % (self.condition.rep(), self.body.rep(), self.else_body.rep())


class Variable(BaseBox):
    def __init__(self, name, state):
        self.name = str(name)
        self.value = None
        self.env = state

    def get_name(self):
        return str(self.name)

    def eval(self, env):
        if dict(self.env.variables).get(self.name) is not None:
            self.value = self.env.variables[self.name]
            return self.value
        raise LogicError("Variable <%s> is not yet defined" % str(self.name))

    def to_string(self):
        return str(self.name)

    def rep(self):
        return 'Variable(%s)' % self.name


class FunctionDeclaration(BaseBox):
    def __init__(self, name, args, block, state):
        self.name = name
        self.args = args
        self.block = block
        state.functions[self.name] = self

    def eval(self, env):
        return self

    def to_string(self):
        return "<function '%s'>" % self.name


class CallFunction(BaseBox):
    def __init__(self, name, args, state):
        self.name = name
        self.args = args
        self.state = state

    def eval(self, env):
        return self.state.functions[self.name].block.eval(env)

    def to_string(self):
        return "<call '%s'>" % self.name


class BaseFunction(BaseBox):
    def __init__(self, expression, state):
        self.expression = expression
        self.value = None
        self.env = state
        self.roundOffDigits = 10

    def eval(self, env):
        raise NotImplementedError("This is abstract method from abstract class BaseFunction(BaseBox){...} !")

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'BaseFunction(%s)' % self.value


class Absolute(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, env):
        import re as regex
        self.value = self.expression.eval(env)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            self.value = abs(self.value)
            return self.value
        else:
            raise ValueError("Cannot abs() not numerical values !")

    def rep(self):
        return 'Absolute(%s)' % self.value


class Sin(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, env):
        import re as regex
        self.value = self.expression.eval(env)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            import math
            self.value = round(math.sin(self.value), self.roundOffDigits)
            return self.value
        else:
            raise ValueError("Cannot sin() not numerical values !")

    def rep(self):
        return 'Sin(%s)' % self.value


class Cos(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, env):
        import re as regex
        self.value = self.expression.eval(env)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            import math
            self.value = round(math.cos(self.value), self.roundOffDigits)
            return self.value
        else:
            raise ValueError("Cannot cos() not numerical values !")

    def rep(self):
        return 'Cos(%s)' % self.value


class Tan(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, env):
        import re as regex
        self.value = self.expression.eval(env)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            import math
            self.value = round(math.tan(self.value), self.roundOffDigits)
            return self.value
        else:
            raise ValueError("Cannot tan() not numerical values !")

    def rep(self):
        return 'Tan(%s)' % self.value


class Pow(BaseFunction):
    def __init__(self, expression, expression2, state):
        super().__init__(expression, state)
        self.expression2 = expression2
        self.value2 = None

    def eval(self, env):
        self.value = self.expression.eval(env)
        self.value2 = self.expression2.eval(env)
        import re as regex
        match1 = regex.search('^-?\d+(\.\d+)?$', str(self.value))
        match2 = regex.search('^-?\d+(\.\d+)?$', str(self.value2))
        if match1 and match2:
            import math
            self.value = math.pow(self.value, self.value2)
            return self.value
        else:
            raise ValueError("Cannot pow() not numerical values !")

    def rep(self):
        return 'Pow(%s)' % self.value


# ABSTRACT CLASS! DO NOT USE!
class Constant(BaseBox):
    def __init__(self, state):
        self.value = None
        self.env = state

    def eval(self, env):
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
            self.value = float(-math.e)
        else:
            self.value = float(math.e)

    def rep(self):
        return '%s(%f)' % (self.name, self.value)


class BinaryOp(BaseBox):
    def __init__(self, left, right, state):
        self.left = left
        self.right = right
        self.state = state


class Assignment(BinaryOp):
    def eval(self, env):
        if isinstance(self.left, Variable):
            var_name = self.left.get_name()
            if dict(self.state.variables).get(var_name) is None:
                self.state.variables[var_name] = self.right.eval(env)
                # print(self.state.variables)
                return self.state.variables  # Return the ParserState() that hold the variables.

            # Otherwise raise error
            raise ImmutableError(var_name)

        else:
            raise LogicError("Cannot assign to <%s>" % self)

    def rep(self):
        return 'Assignment(%s, %s)' % (self.left.rep(), self.right.rep())


class Sum(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) + self.right.eval(env)


class Sub(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) - self.right.eval(env)


class Mul(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) / self.right.eval(env)


class Equal(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) == self.right.eval(env)


class NotEqual(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) != self.right.eval(env)


class GreaterThan(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) > self.right.eval(env)


class LessThan(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) < self.right.eval(env)


class GreaterThanEqual(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) >= self.right.eval(env)


class LessThanEqual(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) <= self.right.eval(env)


class And(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)


class Or(BinaryOp):
    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)


class Not(BaseBox):
    def __init__(self, expression, state):
        self.value = expression.eval(state)
        self.env = state

    def eval(self, env):
        if isinstance(self.value, bool):
            return not bool(self.value)
        raise LogicError("Cannot 'not' that")


class Print(BaseBox):
    def __init__(self, expression=None, state=None):
        self.value = expression
        self.env = state

    def eval(self, env):
        if self.value is None:
            print()
        else:
            print(self.value.eval(env))


class Input(BaseBox):
    def __init__(self, expression=None, state=None):
        self.value = expression
        self.env = state

    def eval(self, env):
        if self.value is None:
            result = input()
        else:
            result = input(self.value.eval(env))

        import re as regex
        if regex.search('^-?\d+(\.\d+)?$', str(result)):
            return float(result)
        else:
            return str(result)
