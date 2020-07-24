from LinearExpression import LinearExpression
from constants import ALMOST_ZERO

class LinearEquation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @classmethod
    def from_string(cls, s):
        left, right = s.split('=')
        left = LinearExpression.from_string(left)
        right = LinearExpression.from_string(right)
        return cls(left=left, right=right)

    def get_first_common_var(self, e2):
        e2vars = e2.vars()
        for var in self.vars():
            if var in e2vars:
                return var
        return None

    def __eq__(self, e2):
        var = self.get_first_common_var(e2)
        if var == None:
            return False
        
        exp1 = self.solve_for(var).right
        exp2 = e2.solve_for(var).right
        return exp1 == exp2


    def __str__(self):
        return str(self.left) + '=' + str(self.right)

    def __repr__(self):
        return "LinearEquation('{0}')".format(self.__str__())

    def __hash__(self):
        return hash(self.__str__())

    def clone(self):
        return LinearEquation(left=self.left.clone(), right=self.right.clone())

    # balances the equation so that the right side = 0
    def zero_form(self):
        result = self.clone()
        return LinearEquation(left = self.left - self.right,
                              right = LinearExpression.from_string('0'))

    def solve_for(self, var):
        if not var in self.vars():
            return None
        result = self.zero_form()
        coe = result.left.terms[var]
        if abs(coe) < ALMOST_ZERO:
            return None
        result.left, result.right = result.right, result.left * -1
        result.right /= coe
        result.left += LinearExpression.from_string(var)
        result.right += LinearExpression.from_string(var)
        return result

    def vars(self):
        return self.left.vars() | self.right.vars()

    def substitute(self, var, expression):
        result = self.clone()
        result.left = result.left.substitute(var, expression)
        result.right = result.right.substitute(var, expression)
        return result

    def is_consistent(self):
        return self.right == self.left
        
    def print_terms(self):
        print(self.terms)

    def simplify(self):
        for k in self.sorted_keys():
            solution = self.solve_for(k)
            if solution:
                break
        return solution
        