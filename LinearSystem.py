from LinearEquation import LinearEquation

MAX_EQUATIONS_IN_SYSTEM = 1000

class NoSolutionError(Exception):
    pass

class InfiniteSolutionsError(Exception):
    pass


class LinearSystem:
    def __init__(self, *equations):
        if not equations:
            equations = []
        self.equations = []
        for eq in equations:
            self.append(eq)
    
    @classmethod
    def from_strings(cls, *equations):
        return cls(*[LinearEquation.from_string(e) for e in equations])

    def __str__(self):
        return ';'.join(str(e) for e in self.equations)

    def __repr__(self):
        return 'LinearSystem('+ self.__str__() +')'
    
    def __eq__(self, s2):
        return set(self.equations) == set(s2.equations)

    def vars(self):
        vars = set()
        for e in self.equations:
            vars |= e.vars()
        return vars


    def append(self, eq):
        if len(self.equations) >= MAX_EQUATIONS_IN_SYSTEM:
            raise Exception('Max equations reached')
        if eq.left == eq.right:
            return
        if not eq in self.equations:
            self.equations.append(eq)


    def solve(self):
        result = []
        equations = self.equations
        
        for count in range(1000):
            if not equations:
                break
            eq = equations.pop()
            var = eq.vars().pop()
            sol = eq.solve_for(var)
            if sol:
                equations2 = []
                for e2 in equations:
                    e3 = e2.substitute(var, sol.right)
                    if e3.vars():
                        equations2.append(e3)
                    else:
                        if not e3.is_consistent():
                            raise NoSolutionError
                if len(sol.vars()) == 1:
                    result.append(sol)
                else:
                    equations2.insert(0, sol)
                equations = equations2

        return LinearSystem(*result)
